from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from backend.config import PipelineConfig

from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import PipelineType, PipelineStep
from backend.application.modules.fetchers.fetcher_spec import FetcherSpec
from backend.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from backend.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec

@dataclass 
class PipelineSpec:
    """Specification for a complete pipeline execution"""
    config: PipelineConfig
    
    # Step-specific specifications
    fetcher_spec: Optional[FetcherSpec] = None
    extraction_spec: Optional[ExtractionSpec] = None
    preprocessor_specs: Optional[List[PreprocessorSpec]] = None  # Multiple speeches
    topic_modeller_spec: Optional[TopicModellerSpec] = None
    
    # Input data (for partial pipelines)
    protocol_ids: Optional[List[UUID]] = None
    speech_ids: Optional[List[UUID]] = None
    corpora_id: Optional[UUID] = None
    
    # Output configuration
    output_corpora_label: Optional[str] = None


@dataclass
class PipelineResult:
    """Result of pipeline execution"""
    success: bool
    pipeline_type: PipelineType
    steps_executed: List[PipelineStep]
    steps_failed: List[PipelineStep]
    
    # Results from each step
    fetched_protocols: Optional[List[UUID]] = None
    extracted_speeches: Optional[List[UUID]] = None 
    preprocessed_speeches: Optional[List[UUID]] = None
    model_results: Optional[Dict[str, Any]] = None
    final_corpora_id: Optional[UUID] = None
    
    # Execution metadata
    execution_time_seconds: Optional[float] = None
    error_messages: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


@dataclass
class StepResult:
    """Result of a single pipeline step"""
    step: PipelineStep
    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None
    execution_time_seconds: Optional[float] = None