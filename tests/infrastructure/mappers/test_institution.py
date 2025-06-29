import unittest
import uuid
from infrastructure.mappers.context.m_institution import InstitutionMapper
from infrastructure.orm.context.orm_institution import InstitutionORM
from domain.models.context.e_institution import Institution
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import InstitutionTypeEnum
from domain.models.common.ve_metadata_plugin import MetadataPlugin
from infrastructure.orm.context.orm_country import CountryORM
from domain.models.common.v_enums import CountryEnum
from infrastructure.orm.context.orm_period import PeriodORM
from datetime import datetime, timezone

def make_institution_orm():
    # Create related country and period objects
    country_id = uuid.uuid4()
    period_id = uuid.uuid4()
    country = CountryORM(id=country_id, name=CountryEnum.GERMANY)
    period = PeriodORM(
        id=period_id,
        name="19th Bundestag",
        start_date=datetime(2017, 10, 24, tzinfo=timezone.utc),
        end_date=datetime(2021, 10, 26, tzinfo=timezone.utc),
        description="19th legislative period of the Bundestag"
    )
    # Main institution
    return InstitutionORM(
        id=uuid.uuid4(),
        country_id=country_id,
        institution_type=InstitutionTypeEnum.PARLIAMENT.value,
        metadata_data={"foo": "bar", "founded": 1949},
        country=country,
        protocols=[],
    )

def make_domain_entity():
    from domain.models.context.ve_period import Period
    from domain.models.common.v_common import DateTime
    period = Period(
        id=UUID(str(uuid.uuid4())),
        start_date=DateTime(datetime(2017, 10, 24, tzinfo=timezone.utc)),
        end_date=DateTime(datetime(2021, 10, 26, tzinfo=timezone.utc)),
        label="19th Bundestag",
        description="19th legislative period of the Bundestag"
    )
    return Institution(
        id=UUID(str(uuid.uuid4())),
        state_id=UUID(str(uuid.uuid4())),
        institution_type=InstitutionTypeEnum.FEDERAL_ASSEMBLY,
        periodisation=[period],
        metadata=MetadataPlugin({"baz": "qux", "founded": 1848})
    )

class TestInstitutionMapper(unittest.TestCase):
    def test_institution_orm_to_domain_conversion(self):
        orm_entity = make_institution_orm()
        domain_entity = InstitutionMapper.to_domain(orm_entity)
        self.assertEqual(domain_entity.id.value, orm_entity.id)
        self.assertEqual(domain_entity.state_id.value, orm_entity.country_id)
        self.assertEqual(domain_entity.institution_type.value, orm_entity.institution_type)
        self.assertEqual(domain_entity.metadata._data, orm_entity.metadata_data)

    def test_institution_domain_to_orm_conversion(self):
        domain_entity = make_domain_entity()
        orm_entity = InstitutionMapper.to_orm(domain_entity)
        self.assertEqual(orm_entity.id, domain_entity.id.value)
        self.assertEqual(orm_entity.country_id, domain_entity.state_id.value)
        self.assertEqual(orm_entity.institution_type, domain_entity.institution_type.value)
        self.assertEqual(orm_entity.metadata_data, domain_entity.metadata._data)

    def test_institution_mapper_back_and_forth(self):
        # Domain -> ORM -> Domain
        original_domain = make_domain_entity()
        orm_entity = InstitutionMapper.to_orm(original_domain)
        mapped_domain = InstitutionMapper.to_domain(orm_entity)
        self.assertEqual(original_domain.id.value, mapped_domain.id.value)
        self.assertEqual(original_domain.state_id.value, mapped_domain.state_id.value)
        self.assertEqual(original_domain.institution_type, mapped_domain.institution_type)
        self.assertEqual(original_domain.metadata._data, mapped_domain.metadata._data)

        # ORM -> Domain -> ORM
        original_orm = make_institution_orm()
        domain_entity = InstitutionMapper.to_domain(original_orm)
        mapped_orm = InstitutionMapper.to_orm(domain_entity)
        self.assertEqual(original_orm.id, mapped_orm.id)
        self.assertEqual(original_orm.country_id, mapped_orm.country_id)
        self.assertEqual(original_orm.institution_type, mapped_orm.institution_type)
        self.assertEqual(original_orm.metadata_data, mapped_orm.metadata_data)

if __name__ == '__main__':
    unittest.main()
