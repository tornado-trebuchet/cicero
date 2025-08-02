from typing import List, Optional

from backend.interface.api.dtos.dto_service import (
    ProtocolSpecDTO,
    ExtractionSpecDTO,
)
from pydantic import BaseModel

class PipelineConfigDTO(BaseModel):
    """DTO for pipeline configuration"""
    pipeline_type: str  # "full", "fetch_extract", "preprocess_model", "extract_preprocess", "custom"
    steps: Optional[List[str]] = None  # For custom pipelines: ["fetch", "extract", "preprocess", "model"]
    continue_on_error: bool = False
    parallel_preprocessing: bool = False
    output_corpora_label: Optional[str] = None


class PipelineSpecDTO(BaseModel):
    """DTO for complete pipeline specification"""
    config: PipelineConfigDTO
    fetcher_spec: Optional[ProtocolSpecDTO] = None
    extraction_spec: Optional[ExtractionSpecDTO] = None
    speech_ids: Optional[List[str]] = None
    corpora_id: Optional[str] = None


class PipelineResultDTO(BaseModel):
    """DTO for pipeline execution results"""
    success: bool
    pipeline_type: str
    steps_executed: List[str]
    steps_failed: List[str]
    fetched_protocols: Optional[List[str]] = None
    extracted_speeches: Optional[List[str]] = None
    preprocessed_speeches: Optional[List[str]] = None
    final_corpora_id: Optional[str] = None
    execution_time_seconds: Optional[float] = None
    error_messages: Optional[List[str]] = None
