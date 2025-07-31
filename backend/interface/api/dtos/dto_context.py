from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel

from backend.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    OwnerTypeEnum,
)


# TODO I strongly sense that pydantic can help makeing it more configurable (filterable ). Read about it later
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


class PartyDTO(BaseModel):
    id: UUID
    country_id: UUID
    party_name: str
    party_program: Optional[str] = None
    speakers: Optional[List[UUID]] = None


class PeriodDTO(BaseModel):
    id: UUID
    owner_id: UUID
    owner_type: OwnerTypeEnum
    label: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SpeakerDTO(BaseModel):
    id: UUID
    country_id: UUID
    name: str
    speeches: Optional[List[UUID]] = None
    party: Optional[UUID] = None
    role: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
