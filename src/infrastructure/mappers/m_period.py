from src.domain.models.ve_period import Period
from src.domain.models.v_common import UUID, DateTime
from src.infrastructure.orm.orm_period import PeriodORM


class PeriodMapper:
    
    @staticmethod
    def to_orm(domain_entity: Period) -> PeriodORM:
        return PeriodORM(
            id=domain_entity.id.value,
            name=domain_entity.label,
            start_date=domain_entity.start_date.value,
            end_date=domain_entity.end_date.value,
            description=domain_entity.description
        )
    
    @staticmethod
    def to_domain(orm_entity: PeriodORM) -> Period:
        return Period(
            id=UUID(str(orm_entity.id)),
            start_date=DateTime(orm_entity.start_date),
            end_date=DateTime(orm_entity.end_date),
            label=orm_entity.name,
            description=orm_entity.description
        )
