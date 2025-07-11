from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from src.domain.models.common.v_enums import ProtocolTypeEnum, LanguageEnum

class ProtocolDTO(BaseModel):
    id: UUID
    institution_id: UUID
    date: datetime
    protocol_type: ProtocolTypeEnum
    protocol_text: str
    agenda: Optional[Dict[str, List[str]]] = None
    file_source: Optional[str] = None  # Accept string for URL
    protocol_speeches: Optional[List[UUID]] = None
    metadata: Optional[Dict[str, Any]] = None

class SpeechTextDTO(BaseModel):
    id: UUID
    speech_id: UUID
    raw_text: UUID
    language_code: LanguageEnum
    clean_text: Optional[UUID] = None
    translated_text: Optional[UUID] = None
    sentences: Optional[UUID] = None
    tokens: Optional[UUID] = None
    ngram_tokens: Optional[UUID] = None
    text_metrics: Optional[dict[str, int | None]] = None

class SpeechDTO(BaseModel):
    id: UUID
    protocol_id: UUID
    speaker_id: UUID
    text: SpeechTextDTO
    metrics: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None
