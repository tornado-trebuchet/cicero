from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.domain.models.common.v_enums import InstitutionTypeEnum

class InstitutionCreateRequest(BaseModel):
    id: str
    country_id: str
    type: InstitutionTypeEnum
    metadata: Optional[Dict[str, Any]] = None

class InstitutionCreateResponse(BaseModel):
    success: bool
    message: str
    institution_id: Optional[str] = None
