from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class SeedDefaultsResponseDTO(BaseModel):
    detail: str

class UUIDResponse(BaseModel):
    id: UUID
    
class CorporaSpecDTO(BaseModel):
    countries: Optional[List[UUID]] = None
    institutions: Optional[List[UUID]] = None
    protocols: Optional[List[UUID]] = None
    parties: Optional[List[UUID]] = None
    speakers: Optional[List[UUID]] = None
    periods: Optional[List[UUID]] = None


class CorporaDTO(BaseModel):
    id: UUID
    label: str
    texts: List[UUID]
    countries: Optional[List[UUID]] = None
    institutions: Optional[List[UUID]] = None
    protocols: Optional[List[UUID]] = None
    parties: Optional[List[UUID]] = None
    speakers: Optional[List[UUID]] = None
    periods: Optional[List[UUID]] = None
