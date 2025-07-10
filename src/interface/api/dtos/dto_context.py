from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum

class CountryDTO(BaseModel):
    id: UUID
    country: CountryEnum
    institutions: Optional[List[UUID]] = None
    periodisation: Optional[List[UUID]] = None
    parties: Optional[List[UUID]] = None 
    speakers: Optional[List[UUID]] = None      

class InstitutionDTO(BaseModel):
    id: UUID
    country_id: UUID
    type: InstitutionTypeEnum
    label: str
    protocols: Optional[List[UUID]] = None
    periodisation: Optional[List[UUID]] = None
    metadata: Optional[dict[str, Any]] = None
