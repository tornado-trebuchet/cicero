from dataclasses import dataclass
from typing import List, Optional

from backend.domain.models.common.v_common import UUID


@dataclass
class CorporaSpec:
    countries: Optional[List[UUID]] = None
    institutions: Optional[List[UUID]] = None
    protocols: Optional[List[UUID]] = None
    parties: Optional[List[UUID]] = None
    speakers: Optional[List[UUID]] = None
    periods: Optional[List[UUID]] = None
