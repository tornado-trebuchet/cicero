from uuid import UUID
from pydantic import BaseModel
from typing import Optional, Dict, Union, Any
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, LanguageEnum, ProtocolTypeEnum

class ProtocolSpecDTO(BaseModel):
    server_base: Optional[str] = None
    endpoint_spec: Optional[str] = None
    full_link: Optional[str] = None
    params: Optional[Dict[str, Union[str, list[str]]]] = None


class ExtractionSpecDTO(BaseModel):
    protocol: UUID
    country: CountryEnum
    institution: InstitutionTypeEnum
    language: LanguageEnum
    protocol_type:  ProtocolTypeEnum
    pattern_spec: Optional[Any] = None
