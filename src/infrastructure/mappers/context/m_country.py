from src.domain.models.common.v_common import UUID
from src.domain.models.context.a_country import Country
from src.infrastructure.orm.context.orm_country import CountryORM


class CountryMapper:
    @staticmethod
    def to_orm(domain_entity: Country) -> CountryORM:
        orm = CountryORM(
            id=domain_entity.id.value, country=domain_entity.country
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: CountryORM) -> Country:
        return Country(
            id=UUID(orm_entity.id),
            country=orm_entity.country,
            institutions=[
                UUID(i.id) for i in getattr(orm_entity, "institutions")
            ],
            periodisation=[
                UUID(p.id) for p in getattr(orm_entity, "periodisation")
            ],
            parties=[UUID(p.id) for p in getattr(orm_entity, "parties")],
            speakers=[UUID(s.id) for s in getattr(orm_entity, "speakers")],
        )
