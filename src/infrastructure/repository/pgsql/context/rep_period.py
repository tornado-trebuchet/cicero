from typing import List, Optional

from src.domain.irepository.context.i_period import IPeriodRepository
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import OwnerTypeEnum
from src.domain.models.context.e_period import Period
from src.domain.models.context.v_label import Label
from src.infrastructure.mappers.context.m_period import PeriodMapper
from src.infrastructure.orm.context.orm_period import PeriodORM
from src.infrastructure.orm.orm_session import session_scope


class PeriodRepository(IPeriodRepository):
    def get_by_id(self, id: UUID) -> Optional[Period]:
        with session_scope() as session:
            orm_period = session.query(PeriodORM).filter_by(id=id.value).one_or_none()
            if orm_period:
                return PeriodMapper.to_domain(orm_period)
            return None

    def get_by_owner_id(self, owner_id: UUID) -> List[Period]:
        with session_scope() as session:
            orm_periods = session.query(PeriodORM).filter_by(owner_id=owner_id.value).all()
            return [PeriodMapper.to_domain(orm) for orm in orm_periods]

    def get_by_owner(self, owner_id: UUID, owner_type: OwnerTypeEnum) -> List[Period]:
        """Get periods by specific owner type and id"""
        with session_scope() as session:
            orm_periods = (
                session.query(PeriodORM).filter_by(owner_id=owner_id.value, owner_type=owner_type).all()
            )
            return [PeriodMapper.to_domain(orm) for orm in orm_periods]

    def get_by_label(self, label: Label) -> Optional[Period]:
        with session_scope() as session:
            orm_period = session.query(PeriodORM).filter_by(label=label.value).one_or_none()
            if orm_period:
                return PeriodMapper.to_domain(orm_period)
            return None

    def list(self) -> List[Period]:
        with session_scope() as session:
            orm_periods = session.query(PeriodORM).all()
            return [PeriodMapper.to_domain(orm) for orm in orm_periods]

    def add(self, period: Period) -> None:
        with session_scope() as session:
            orm_period = PeriodMapper.to_orm(period)
            session.add(orm_period)

    def update(self, period: Period) -> None:
        with session_scope() as session:
            exists = session.query(PeriodORM).filter_by(id=period.id.value).one_or_none()
            if not exists:
                raise ValueError(f"Period with id {period.id} not found.")
            orm_period = PeriodMapper.to_orm(period)
            session.merge(orm_period)

    def delete(self, id: UUID) -> None:
        with session_scope() as session:
            orm_period = session.query(PeriodORM).filter_by(id=id.value).one_or_none()
            if orm_period:
                session.delete(orm_period)
