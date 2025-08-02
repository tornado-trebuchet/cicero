from typing import List, Optional

from backend.application.pipeline.spec import (
    PipelineSpec,
    PipelineConfig,
    PipelineType,
    PipelineStep
)
from backend.application.modules.fetchers.fetcher_spec import FetcherSpec
from backend.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec
from backend.domain.models.common.v_common import UUID


class PipelineFactory:
    """Factory for creating common pipeline configurations"""
    
    @staticmethod
    def create_full_pipeline(
        fetcher_spec: FetcherSpec,
        extraction_spec: ExtractionSpec,
        topic_modeller_spec: TopicModellerSpec,
        continue_on_error: bool = False,
        parallel_preprocessing: bool = False
    ) -> PipelineSpec:
        """Create a full pipeline: Fetch → Extract → Preprocess → Model"""
        
        config = PipelineConfig(
            pipeline_type=PipelineType.FULL,
            parallel_preprocessing=parallel_preprocessing,
            continue_on_error=continue_on_error,
            save_intermediate_results=True
        )
        
        return PipelineSpec(
            config=config,
            fetcher_spec=fetcher_spec,
            extraction_spec=extraction_spec,
            topic_modeller_spec=topic_modeller_spec
        )
    
    @staticmethod
    def create_custom_pipeline(
        steps: List[PipelineStep],
        fetcher_spec: Optional[FetcherSpec] = None,
        extraction_spec: Optional[ExtractionSpec] = None,
        topic_modeller_spec: Optional[TopicModellerSpec] = None,
        speech_ids: Optional[List[UUID]] = None,
        protocol_ids: Optional[List[UUID]] = None
    ) -> PipelineSpec:
        """Create a custom pipeline with specific steps"""
        
        config = PipelineConfig(
            pipeline_type=PipelineType.CUSTOM,
            steps=steps,
            continue_on_error=True,
            save_intermediate_results=True
        )
        
        return PipelineSpec(
            config=config,
            fetcher_spec=fetcher_spec,
            extraction_spec=extraction_spec,
            topic_modeller_spec=topic_modeller_spec,
            speech_ids=speech_ids,
            protocol_ids=protocol_ids
        )
