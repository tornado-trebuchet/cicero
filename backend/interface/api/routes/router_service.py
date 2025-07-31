from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.application.di.di_service import get_bundestag_fetcher, get_preprocessor
from backend.application.modules.text_services.extractor.extractor import (
    ExtractorService,
)
from backend.interface.api.dtos.dto_service import (
    ExtractionSpecDTO,
    ProtocolSpecDTO,
    PreprocessorSpecDTO,
)
from backend.interface.api.dtos.dto_text import ProtocolDTO, SpeechDTO, CleanTextDTO
from backend.interface.api.mappers.mp_service import (
    dto_to_extraction_spec,
    dto_to_protocol_spec,
    dto_to_preprocessor_spec,
)
from backend.interface.api.mappers.mp_text import protocol_to_dto, speech_to_dto, clean_text_to_dto
from backend.domain.models.common.v_common import UUID
from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_speech_metrics import SpeechMetricsRepository
from backend.domain.services.modelling.topic_modeller_bert import TopicModeler
from backend.application.modules.modellers.topic_modeller.topic_modeller import TopicModeller
from backend.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec

service_router = APIRouter()

# TODO: This is an absolutely lazy ass disaster. Need to build a proper pipeline AND SO REPOSITORIES DO NOT EXIST HERE IN CODE
@service_router.post("/service/fetcher/bundestag", response_model=ProtocolDTO)
def fetch_bundestag_protocol(protocol_spec: ProtocolSpecDTO):
    try:
        spec = dto_to_protocol_spec(protocol_spec)
        fetcher = get_bundestag_fetcher(spec)
        protocol = fetcher.fetch_single()
        return protocol_to_dto(protocol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching protocol failed: {str(e)}")


def fetch_bundestag_protocols(protocol_spec: ProtocolSpecDTO):
    try:
        spec = dto_to_protocol_spec(protocol_spec)
        fetcher = get_bundestag_fetcher(spec)
        return fetcher.fetch_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetching protocols failed: {str(e)}")

@service_router.post("/service/extractor/speeches", response_model=list[SpeechDTO])
def extract_speeches(extraction_spec: ExtractionSpecDTO):
    try:
        spec = dto_to_extraction_spec(extraction_spec)
        extractor_service = ExtractorService()
        speeches = extractor_service.extract_speeches(spec)
        return [speech_to_dto(s) for s in speeches]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech extraction failed: {str(e)}")


@service_router.post("/service/preprocessor/raw_text", response_model=CleanTextDTO)
def preprocess_raw_text(preprocessor_spec: PreprocessorSpecDTO):
    try:
        spec = dto_to_preprocessor_spec(preprocessor_spec)
        # Manually delete clean text by speech before preprocessing
        clean_text_repo = CleanTextRepository()  #
        existing_clean = clean_text_repo.get_by_speech_id(spec.speech)  #
        if existing_clean:  #
            clean_text_repo.delete(existing_clean.id)  #
        # Remove after develop ^
        preprocessor_service = get_preprocessor(spec)
        clean_text = preprocessor_service.execute()
        return clean_text_to_dto(clean_text)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")

@service_router.post("/service/preprocessor/corpora/{corpora_id}")
def preprocess_corpora(corpora_id: str):
    def result_stream():
        corpora_repo = CorporaRepository()
        corpora = corpora_repo.get_by_id(UUID(corpora_id))
        if not corpora:
            yield f"{{'speech_id': None, 'status': 'error', 'error': 'Corpora not found'}}\n"
            return
        for speech_id in corpora.texts:
            try:
                spec = PreprocessorSpec(speech=speech_id)
                preprocessor_service = get_preprocessor(spec)
                preprocessor_service.execute()
                yield f"{{'speech_id': '{speech_id}', 'status': 'success'}}\n"
            except Exception as e:
                yield f"{{'speech_id': '{speech_id}', 'status': 'error', 'error': '{str(e)}'}}\n"
    return StreamingResponse(result_stream(), media_type="text/plain")

# TODO: add DI 
@service_router.post("/service/topic-modelling/{corpora_id}")
def topic_modelling(corpora_id: str):
    try:
        # Fetch corpora
        corpora_repo = CorporaRepository()
        corpora = corpora_repo.get_by_id(UUID(corpora_id))
        if not corpora:
            raise HTTPException(status_code=404, detail="Corpora not found")
        # Prepare dependencies
        clean_text_repo = CleanTextRepository()
        speech_metrics_repo = SpeechMetricsRepository()
        topic_modeler = TopicModeler()
        modeller = TopicModeller(corpora_repo, clean_text_repo, speech_metrics_repo, topic_modeler)
        # Fit model and annotate
        result = modeller.build_model_and_annotate(TopicModellerSpec(corpora=corpora))
        annotated = result["annotated_corpora"]
        # Return a summary (could be improved with a DTO)
        return {"corpora_id": corpora_id, "num_texts": len(annotated.texts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic modelling failed: {str(e)}")
