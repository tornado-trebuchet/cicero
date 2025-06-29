from domain.models.context.e_country import Country
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import CountryEnum
from infrastructure.orm.context.orm_country import CountryORM


class CountryMapper:
    
    @staticmethod
    def to_orm(domain_entity: Country) -> CountryORM:
        return CountryORM(
            id=domain_entity.id.value,
            name=domain_entity.country
        )
    
    @staticmethod
    def to_domain(orm_entity: CountryORM) -> Country:
        return Country(
            id=UUID(str(orm_entity.id)),
            country=CountryEnum(orm_entity.name)
        )