from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from src.interface.api.dtos.dto_text import ProtocolDTO, SpeechTextDTO, SpeechDTO
from src.interface.api.mappers.mp_text import protocol_to_dto, speech_text_to_dto, speech_to_dto
from src.application.di.di_text import (
    get_protocol_by_id_use_case,
    get_protocols_by_country_id_use_case,
    get_protocols_by_institution_id_use_case,
    get_protocols_by_institution_and_period_use_case,
    get_protocols_by_date_range_use_case,
    get_list_protocols_use_case,
    get_speech_text_by_id_use_case,
    get_speech_by_id_use_case,
    get_speeches_by_protocol_id_use_case,
    get_speeches_by_speaker_id_use_case,
    get_speeches_by_date_range_use_case,
)
from src.domain.models.common.v_common import UUID, DateTime

text_router = APIRouter()

@text_router.get("/protocols/{protocol_id}", response_model=ProtocolDTO)
def get_protocol_by_id(protocol_id: str, use_case: Any = Depends(get_protocol_by_id_use_case)) -> ProtocolDTO:
    protocol = use_case.execute(UUID(protocol_id))
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    return protocol_to_dto(protocol)

@text_router.get("/protocols/by_country/{country_id}", response_model=List[ProtocolDTO])
def get_protocols_by_country_id(country_id: str, use_case: Any = Depends(get_protocols_by_country_id_use_case)) -> List[ProtocolDTO]:
    protocols = use_case.execute(UUID(country_id))
    return [protocol_to_dto(p) for p in protocols]

@text_router.get("/protocols/by_institution/{institution_id}", response_model=List[ProtocolDTO])
def get_protocols_by_institution_id(institution_id: str, use_case: Any = Depends(get_protocols_by_institution_id_use_case)) -> List[ProtocolDTO]:
    protocols = use_case.execute(UUID(institution_id))
    return [protocol_to_dto(p) for p in protocols]

@text_router.get("/protocols/by_institution_and_period/{institution_id}/{period_id}", response_model=List[ProtocolDTO])
def get_protocols_by_institution_and_period(
    institution_id: str,
    period_id: str,
    use_case: Any = Depends(get_protocols_by_institution_and_period_use_case),
) -> List[ProtocolDTO]:
    protocols = use_case.execute(UUID(institution_id), UUID(period_id))
    return [protocol_to_dto(p) for p in protocols]

@text_router.get("/protocols/by_date_range/{start_date}/{end_date}", response_model=List[ProtocolDTO])
def get_protocols_by_date_range(
    start_date: str,
    end_date: str,
    use_case: Any = Depends(get_protocols_by_date_range_use_case),
) -> List[ProtocolDTO]:
    protocols = use_case.execute(DateTime(start_date), DateTime(end_date))
    return [protocol_to_dto(p) for p in protocols]

@text_router.get("/protocols", response_model=List[ProtocolDTO])
def list_protocols(list_protocols_use_case: Any = Depends(get_list_protocols_use_case)) -> List[ProtocolDTO]:
    protocols = list_protocols_use_case.execute()
    return [protocol_to_dto(p) for p in protocols]

@text_router.get("/speech_texts/{speech_text_id}", response_model=SpeechTextDTO)
def get_speech_text_by_id(speech_text_id: str, use_case: Any = Depends(get_speech_text_by_id_use_case)) -> SpeechTextDTO:
    speech_text = use_case.execute(UUID(speech_text_id))
    if not speech_text:
        raise HTTPException(status_code=404, detail="SpeechText not found")
    return speech_text_to_dto(speech_text)

@text_router.get("/speeches/{speech_id}", response_model=SpeechDTO)
def get_speech_by_id(speech_id: str, use_case: Any = Depends(get_speech_by_id_use_case)) -> SpeechDTO:
    speech = use_case.execute(UUID(speech_id))
    if not speech:
        raise HTTPException(status_code=404, detail="Speech not found")
    return speech_to_dto(speech)

@text_router.get("/speeches/by_protocol/{protocol_id}", response_model=List[SpeechDTO])
def get_speeches_by_protocol_id(protocol_id: str, use_case: Any = Depends(get_speeches_by_protocol_id_use_case)) -> List[SpeechDTO]:
    speeches = use_case.execute(UUID(protocol_id))
    return [speech_to_dto(s) for s in speeches]

@text_router.get("/speeches/by_speaker/{speaker_id}", response_model=List[SpeechDTO])
def get_speeches_by_speaker_id(speaker_id: str, use_case: Any = Depends(get_speeches_by_speaker_id_use_case)) -> List[SpeechDTO]:
    speeches = use_case.execute(UUID(speaker_id))
    return [speech_to_dto(s) for s in speeches]

@text_router.get("/speeches/by_date_range/{start_date}/{end_date}", response_model=List[SpeechDTO])
def get_speeches_by_date_range(start_date: str, end_date: str, use_case: Any = Depends(get_speeches_by_date_range_use_case)) -> List[SpeechDTO]:
    speeches = use_case.execute(DateTime(start_date), DateTime(end_date))
    return [speech_to_dto(s) for s in speeches]
