from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.context.e_period import Period
from src.domain.models.context.v_label import Label
from src.infrastructure.orm.context.orm_period import PeriodORM


class PeriodMapper:
    @staticmethod
    def to_orm(domain_entity: Period) -> PeriodORM:
        orm = PeriodORM(
            id=domain_entity.id.value,
            owner_id=domain_entity.owner_id.value,
            owner_type=domain_entity.owner_type,
            label=domain_entity.label.value,
            start_date=domain_entity.start_date.value,
            end_date=domain_entity.end_date.value,
            description=domain_entity.description,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: PeriodORM) -> Period:
        return Period(
            id=UUID(orm_entity.id),
            owner_id=UUID(orm_entity.owner_id),
            owner_type=orm_entity.owner_type,
            label=Label(orm_entity.label),
            start_date=DateTime(orm_entity.start_date),
            end_date=DateTime(orm_entity.end_date),
            description=orm_entity.description,
        )
