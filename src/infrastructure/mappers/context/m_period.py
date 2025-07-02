from src.domain.models.context.v_period import Period
from src.domain.models.common.v_common import UUID, DateTime
from src.infrastructure.orm.context.orm_period import PeriodORM


class PeriodMapper:
    
    @staticmethod
    def to_orm(domain_entity: Period) -> PeriodORM:
        return PeriodORM(
            label=domain_entity.label,
            start_date=domain_entity.start_date.value,
            end_date=domain_entity.end_date.value,
            description=domain_entity.description
        )
    
    @staticmethod
    def to_domain(orm_entity: PeriodORM) -> Period:
        return Period(
            label=orm_entity.label,
            start_date=DateTime(orm_entity.start_date),
            end_date=DateTime(orm_entity.end_date),
            description=orm_entity.description
        )
