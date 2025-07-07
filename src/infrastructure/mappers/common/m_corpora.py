from typing import Set, Optional, List
from sqlalchemy.orm import Session
from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from domain.models.context.e_period import Period
from src.infrastructure.orm.common.orm_corpora import CorporaORM


class CorporaMapper:
    """Mapper for converting between Corpora domain model and CorporaORM."""
    