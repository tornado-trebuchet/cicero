from typing import Any
from dataclasses import dataclass
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, LanguageEnum, ProtocolTypeEnum
from src.domain.models.common.v_common import UUID

# THIS CAN BE REDUCED TO THE PROTOCOL ID 
@dataclass
class ExtractionSpec:
    protocol: UUID
    country: CountryEnum
    institution: InstitutionTypeEnum
    language: LanguageEnum
    protocol_type: ProtocolTypeEnum
    pattern_spec: Any
