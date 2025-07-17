from typing import Any
from dataclasses import dataclass
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, LanguageEnum
from src.domain.models.common.v_common import UUID

@dataclass
class ExtractionSpec:
    protocol: UUID
    country: CountryEnum
    institution: InstitutionTypeEnum
    language: LanguageEnum
    pattern_spec: Any
