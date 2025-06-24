import unittest
import uuid
from src.infrastructure.mappers.m_country import CountryMapper
from src.infrastructure.orm.orm_country import CountryORM
from src.domain.models.e_country import Country
from src.domain.models.v_common import UUID
from src.domain.models.v_enums import CountryEnum


def make_country_orm():
    """Factory function to create a CountryORM instance for testing."""
    return CountryORM(
        id=uuid.uuid4(),
        name=CountryEnum.GERMANY
    )

def make_domain_entity():
    """Factory function to create a Country domain entity for testing."""
    return Country(
        id=UUID(str(uuid.uuid4())),
        country=CountryEnum.FRANCE
    )


class TestCountryMapper(unittest.TestCase):
    
    def test_country_orm_to_domain_conversion(self):
        orm_entity = make_country_orm()
        domain_entity = CountryMapper.to_domain(orm_entity)
        self.assertEqual(domain_entity.id.value, orm_entity.id)
        self.assertEqual(domain_entity.country, orm_entity.name)

    def test_country_domain_to_orm_conversion(self):
        domain_entity = make_domain_entity()
        orm_entity = CountryMapper.to_orm(domain_entity)
        self.assertEqual(orm_entity.id, domain_entity.id.value)
        self.assertEqual(orm_entity.name, domain_entity.country)

    def test_country_mapper_back_and_forth(self):
        # Domain -> ORM -> Domain
        original_domain = make_domain_entity()
        orm_entity = CountryMapper.to_orm(original_domain)
        mapped_domain = CountryMapper.to_domain(orm_entity)
        self.assertEqual(original_domain.id.value, mapped_domain.id.value)
        self.assertEqual(original_domain.country, mapped_domain.country)

        # ORM -> Domain -> ORM
        original_orm = make_country_orm()
        domain_entity = CountryMapper.to_domain(original_orm)
        mapped_orm = CountryMapper.to_orm(domain_entity)
        self.assertEqual(original_orm.id, mapped_orm.id)
        self.assertEqual(original_orm.name, mapped_orm.name)


if __name__ == '__main__':
    unittest.main()