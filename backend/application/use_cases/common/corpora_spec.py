from dataclasses import dataclass
from typing import List, Optional

from backend.domain.models.common.v_common import UUID

#TODO: Make it do magic with finding shit by strings 
#TODO: Make a translating class between these two Label function is sort of there ACTUALLY HOLD MY BALLS I'll sleep on it 

@dataclass
class CorporaSpec:
    countries: Optional[List[UUID]] = None
    institutions: Optional[List[UUID]] = None
    protocols: Optional[List[UUID]] = None
    parties: Optional[List[UUID]] = None
    speakers: Optional[List[UUID]] = None
    periods: Optional[List[UUID]] = None

@dataclass
class HumanReadableCorporaSpec:
    label: str
    countries: Optional[List[str]] = None
    institutions: Optional[List[str]] = None
    protocols: Optional[List[str]] = None
    parties: Optional[List[str]] = None
    speakers: Optional[List[str]] = None
    periods: Optional[List[str]] = None
