from fastapi import APIRouter, HTTPException

from src.application.di.di_service import get_bundestag_fetcher, get_preprocessor
from src.application.modules.text_services.extractor.extractor import (
    ExtractorService,
)
from src.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
    PreprocessorSpecDTO,
)
from src.interface.api.dtos.dto_text import ProtocolDTO, SpeechDTO, CleanTextDTO
from src.interface.api.mappers.mp_service import (
    dto_to_extraction_spec,
    dto_to_protocol_spec,
    dto_to_preprocessor_spec
)
from src.interface.api.mappers.mp_text import protocol_to_dto, speech_to_dto, clean_text_to_dto
from src.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository

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
def extract_speeches(extraction_spec: ExtractionSpecDTO):
    try:
        spec = dto_to_extraction_spec(extraction_spec)
        extractor_service = ExtractorService()
        speeches = extractor_service.extract_speeches(spec)
        return [speech_to_dto(s) for s in speeches]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Speech extraction failed: {str(e)}"
        )

@service_router.post(
    "/service/preprocessor/raw_text", response_model=CleanTextDTO
)
def preprocess_raw_text(preprocessor_spec: PreprocessorSpecDTO):
    try:
        spec = dto_to_preprocessor_spec(preprocessor_spec)
        # Manually delete clean text by speech before preprocessing
        clean_text_repo = CleanTextRepository() #
        existing_clean = clean_text_repo.get_by_speech_id(spec.speech) #
        if existing_clean: # 
            clean_text_repo.delete(existing_clean.id) # 
        # Remove after develop ^
        preprocessor_service = get_preprocessor(spec)
        clean_text = preprocessor_service.execute()
        return clean_text_to_dto(clean_text)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")