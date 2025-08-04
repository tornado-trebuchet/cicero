import time
import logging
from typing import List, Dict, Optional

from backend.application.di import di_service
from backend.application.pipeline.spec import (
    PipelineSpec, 
    PipelineResult, 
    StepResult, 
    PipelineStep, 
    PipelineType
)
from backend.domain.models.common.v_common import UUID
from backend.application.modules.text_services.extractor.extractor import ExtractorService
from backend.application.modules.modellers.topic_modeller.topic_modeller import TopicModeller
from backend.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_speech_metrics import SpeechMetricsRepository
from backend.domain.services.modelling.topic_modeller_bert import TopicModeler

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Orchestrates the data flow: Fetching -> Extracting -> Preprocessing -> Modelling.
    Instantiates and wires up application services using config and spec.
    """
    
    def __init__(self, 
                 extractor_service: Optional[ExtractorService] = None, # FIXME: Not in DI 
                 corpora_repo: Optional[CorporaRepository] = None,
                 clean_text_repo: Optional[CleanTextRepository] = None,
                 speech_metrics_repo: Optional[SpeechMetricsRepository] = None,
                 topic_modeler: Optional[TopicModeler] = None): # FIXME: Not in DI
        self.steps_executed: List[PipelineStep] = []
        self.results: Dict[PipelineStep, StepResult] = {}
        
        self._extractor_service = extractor_service
        self._corpora_repo = corpora_repo
        self._clean_text_repo = clean_text_repo
        self._speech_metrics_repo = speech_metrics_repo
        self._topic_modeler = topic_modeler
        
    def execute(self, spec: PipelineSpec) -> PipelineResult:
        """Execute the pipeline according to the specification"""
        start_time = time.time()
        logger.info(f"Starting pipeline execution: {spec.config.pipeline_type}")
        
        try:
            # Determine steps to execute
            steps = self._determine_steps(spec)
            
            # Execute each step
            for step in steps:
                step_result = self._execute_step(step, spec)
                self.results[step] = step_result
                self.steps_executed.append(step)
                
                if not step_result.success and not spec.config.continue_on_error:
                    logger.error(f"Pipeline failed at step {step}: {step_result.error_message}")
                    break
                    
                if spec.config.save_intermediate_results:
                    logger.info(f"Step {step} completed successfully")
            
            # Build final result
            result = self._build_result(spec, start_time)
            logger.info(f"Pipeline execution completed in {result.execution_time_seconds:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            return PipelineResult(
                success=False,
                pipeline_type=spec.config.pipeline_type,
                steps_executed=self.steps_executed,
                steps_failed=[step for step in self.steps_executed if not self.results[step].success],
                execution_time_seconds=time.time() - start_time,
                error_messages=[str(e)]
            )
    
    def _determine_steps(self, spec: PipelineSpec) -> List[PipelineStep]:
        """Determine which steps to execute based on pipeline type"""
        if spec.config.pipeline_type == PipelineType.CUSTOM and spec.config.steps:
            return spec.config.steps
        elif spec.config.pipeline_type == PipelineType.FULL:
            return [PipelineStep.FETCH, PipelineStep.EXTRACT, PipelineStep.PREPROCESS, PipelineStep.TOPIC_MODEL]
        elif spec.config.pipeline_type == PipelineType.FETCH: 
            return [PipelineStep.FETCH]
        elif spec.config.pipeline_type == PipelineType.EXTRACT:
            return [PipelineStep.EXTRACT]
        elif spec.config.pipeline_type == PipelineType.PREPROCESS:
            return [PipelineStep.PREPROCESS]
        elif spec.config.pipeline_type == PipelineType.TOPIC_MODEL:
            return [PipelineStep.TOPIC_MODEL]
        else:
            raise ValueError(f"Unknown pipeline type: {spec.config.pipeline_type}")
    
    def _execute_step(self, step: PipelineStep, spec: PipelineSpec) -> StepResult:
        """Execute a single pipeline step"""
        start_time = time.time()
        
        try:
            if step == PipelineStep.FETCH:
                return self._execute_fetch_step(spec, start_time)
            elif step == PipelineStep.EXTRACT:
                return self._execute_extract_step(spec, start_time)
            elif step == PipelineStep.PREPROCESS:
                return self._execute_preprocess_step(spec, start_time)
            elif step == PipelineStep.TOPIC_MODEL:
                return self._execute_model_step(spec, start_time)
            else:
                raise ValueError(f"Unknown step: {step}")
                
        except Exception as e:
            return StepResult(
                step=step,
                success=False,
                error_message=str(e),
                execution_time_seconds=time.time() - start_time
            )
    
    def _execute_fetch_step(self, spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute the fetch step"""
        if not spec.fetcher_spec:
            raise ValueError("Fetcher spec required for fetch step")
            
        fetcher = di_service.get_bundestag_fetcher(spec.fetcher_spec)
        
        # BundestagFetcher.fetch_list() returns List[UUID], fetch_single() returns Protocol
        if hasattr(fetcher, 'fetch_list'):
            protocol_ids = fetcher.fetch_list()  # Returns List[UUID]
        else:
            protocol = fetcher.fetch_single()   # Returns Protocol
            protocol_ids = [protocol.id]
            
        return StepResult(
            step=PipelineStep.FETCH,
            success=True,
            data=protocol_ids,
            execution_time_seconds=time.time() - start_time
        )
    
    def _execute_extract_step(self, spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute the extract step"""
        if not spec.extraction_spec:
            raise ValueError("Extraction spec required for extract step")
            
        extractor = ExtractorService()
        speeches = extractor.extract_speeches(spec.extraction_spec)
        speech_ids = [s.id for s in speeches]
        
        return StepResult(
            step=PipelineStep.EXTRACT,
            success=True,
            data=speech_ids,
            execution_time_seconds=time.time() - start_time
        )
    
    def _execute_preprocess_step(self, spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute the preprocess step"""
        speech_ids: List[UUID] = []
        
        # Get speech IDs from previous step or spec
        if PipelineStep.EXTRACT in self.results:
            speech_ids = self.results[PipelineStep.EXTRACT].data or []
        elif spec.speech_ids:
            speech_ids = spec.speech_ids
        else:
            raise ValueError("No speech IDs available for preprocessing")
        
        if spec.config.parallel_preprocessing and spec.config.batch_size:
            return self._execute_preprocess_parallel(speech_ids, spec, start_time)
        else:
            return self._execute_preprocess_sequential(speech_ids, spec, start_time)
    
    def _execute_preprocess_sequential(self, speech_ids: List[UUID], spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute preprocessing sequentially"""
        processed_speeches: List[UUID] = []
        errors: List[str] = []
        
        for speech_id in speech_ids:
            try:
                preprocessor_spec = PreprocessorSpec(speech=speech_id)
                preprocessor = di_service.get_preprocessor(preprocessor_spec)
                preprocessor.execute()  # Creates CleanText in database
                processed_speeches.append(speech_id)
                
            except Exception as e:
                error_msg = f"Failed to preprocess speech {speech_id}: {str(e)}"
                errors.append(error_msg)
                logger.warning(error_msg)
                
                if not spec.config.continue_on_error:
                    raise
        
        return StepResult(
            step=PipelineStep.PREPROCESS,
            success=len(processed_speeches) > 0,
            data=processed_speeches,
            execution_time_seconds=time.time() - start_time
        )
    # FIXME: get corpora instead of lists
    def _execute_preprocess_parallel(self, speech_ids: List[UUID], spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute preprocessing in parallel batches"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        processed_speeches: List[UUID] = []
        errors: List[str] = []
        batch_size = spec.config.batch_size or 10
        
        def process_speech(speech_id: UUID) -> Optional[UUID]:
            try:
                preprocessor_spec = PreprocessorSpec(speech=speech_id)
                preprocessor = di_service.get_preprocessor(preprocessor_spec)
                preprocessor.execute()
                return speech_id
            except Exception as e:
                error_msg = f"Failed to preprocess speech {speech_id}: {str(e)}"
                logger.warning(error_msg)
                if not spec.config.continue_on_error:
                    raise
                return None
        
        # Process in batches to avoid overwhelming the system
        for i in range(0, len(speech_ids), batch_size):
            batch = speech_ids[i:i + batch_size]
            
            with ThreadPoolExecutor(max_workers=min(len(batch), 5)) as executor:
                future_to_speech = {executor.submit(process_speech, speech_id): speech_id 
                                  for speech_id in batch}
                
                for future in as_completed(future_to_speech):
                    try:
                        result = future.result()
                        if result:
                            processed_speeches.append(result)
                    except Exception as e:
                        speech_id = future_to_speech[future]
                        error_msg = f"Failed to preprocess speech {speech_id}: {str(e)}"
                        errors.append(error_msg)
        
        return StepResult(
            step=PipelineStep.PREPROCESS,
            success=len(processed_speeches) > 0,
            data=processed_speeches,
            execution_time_seconds=time.time() - start_time
        )
    
    def _execute_model_step(self, spec: PipelineSpec, start_time: float) -> StepResult:
        """Execute the modeling step"""
        if not spec.topic_modeller_spec:
            raise ValueError("Topic modeller spec required for model step")
        
        # Prepare dependencies
        corpora_repo = CorporaRepository()
        clean_text_repo = CleanTextRepository()
        speech_metrics_repo = SpeechMetricsRepository()
        topic_modeler = TopicModeler()
        
        modeller = TopicModeller(corpora_repo, clean_text_repo, speech_metrics_repo, topic_modeler)
        result = modeller.build_model_and_annotate(spec.topic_modeller_spec)
        
        return StepResult(
            step=PipelineStep.TOPIC_MODEL,
            success=True,
            data=result,
            execution_time_seconds=time.time() - start_time
        )
    
    def _build_result(self, spec: PipelineSpec, start_time: float) -> PipelineResult:
        """Build the final pipeline result"""
        failed_steps = [step for step, result in self.results.items() if not result.success]
        success = len(failed_steps) == 0
        
        # Extract data from step results
        fetched_protocols = None
        extracted_speeches = None
        preprocessed_speeches = None
        model_results = None
        
        if PipelineStep.FETCH in self.results:
            fetched_protocols = self.results[PipelineStep.FETCH].data
            
        if PipelineStep.EXTRACT in self.results:
            extracted_speeches = self.results[PipelineStep.EXTRACT].data
            
        if PipelineStep.PREPROCESS in self.results:
            preprocessed_speeches = self.results[PipelineStep.PREPROCESS].data
            
        if PipelineStep.TOPIC_MODEL in self.results:
            model_results = self.results[PipelineStep.TOPIC_MODEL].data
        
        # Collect error messages
        error_messages: List[str] = []
        for result in self.results.values():
            if result.error_message:
                error_messages.append(result.error_message)
        
        return PipelineResult(
            success=success,
            pipeline_type=spec.config.pipeline_type,
            steps_executed=self.steps_executed,
            steps_failed=failed_steps,
            fetched_protocols=fetched_protocols,
            extracted_speeches=extracted_speeches,
            preprocessed_speeches=preprocessed_speeches,
            model_results=model_results,
            execution_time_seconds=time.time() - start_time,
            error_messages=error_messages if error_messages else None
        )
