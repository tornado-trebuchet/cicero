from dataclasses import dataclass
from typing import Any
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum, LanguageEnum

@dataclass
class ExtractionSpec:
    country: CountryEnum
    institution: InstitutionTypeEnum
    language: LanguageEnum
    pattern_spec: Any
