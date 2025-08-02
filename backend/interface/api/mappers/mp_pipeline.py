from backend.application.pipeline.spec import PipelineResult
from backend.interface.api.dtos.dto_pipeline import PipelineResultDTO

def pipeline_result_to_dto(result: PipelineResult) -> PipelineResultDTO:
    """Convert pipeline result to DTO"""
    return PipelineResultDTO(
        success=result.success,
        pipeline_type=result.pipeline_type.value,
        steps_executed=[step.value for step in result.steps_executed],
        steps_failed=[step.value for step in result.steps_failed],
        fetched_protocols=[str(pid) for pid in result.fetched_protocols] if result.fetched_protocols else None,
        extracted_speeches=[str(sid) for sid in result.extracted_speeches] if result.extracted_speeches else None,
        preprocessed_speeches=[str(sid) for sid in result.preprocessed_speeches] if result.preprocessed_speeches else None,
        final_corpora_id=str(result.final_corpora_id) if result.final_corpora_id else None,
        execution_time_seconds=result.execution_time_seconds,
        error_messages=result.error_messages
    )