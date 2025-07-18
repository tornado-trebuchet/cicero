from fastapi import APIRouter, HTTPException

from src.application.di.di_service import get_bundestag_fetcher
from src.application.modules.text_services.extractor.extractor import (
    ExtractorService,
)
from src.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
)
from src.interface.api.dtos.dto_text import ProtocolDTO, SpeechDTO
from src.interface.api.mappers.mp_service import (
    dto_to_extraction_spec,
    dto_to_protocol_spec,
)
from src.interface.api.mappers.mp_text import protocol_to_dto, speech_to_dto

service_router = APIRouter()


@service_router.post("/service/fetcher/bundestag", response_model=ProtocolDTO)
def fetch_bundestag_protocol(protocol_spec: ProtocolSpecDTO):
    try:
        spec = dto_to_protocol_spec(protocol_spec)
        fetcher = get_bundestag_fetcher(spec)
        protocol = fetcher.fetch_single()
        return protocol_to_dto(protocol)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Fetching protocol failed: {str(e)}"
        )


@service_router.post(
    "/service/extractor/speeches", response_model=list[SpeechDTO]
)
def extract_speeches_api(extraction_spec: ExtractionSpecDTO):
    try:
        spec = dto_to_extraction_spec(extraction_spec)
        extractor_service = ExtractorService()
        speeches = extractor_service.extract_speeches(spec)
        return [speech_to_dto(s) for s in speeches]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Speech extraction failed: {str(e)}"
        )
