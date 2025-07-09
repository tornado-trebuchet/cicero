from pydantic import BaseModel
from typing import Optional, List
from src.domain.models.common.v_enums import CountryEnum

class CountryCreateRequest(BaseModel):
    id: str
    country: CountryEnum
    periodisation: Optional[List[str]] = None
    institutions: Optional[List[str]] = None
    parties: Optional[List[str]] = None
    speakers: Optional[List[str]] = None

class CountryCreateResponse(BaseModel):
    success: bool
    message: str
    country_id: Optional[str] = None
