import unittest
import uuid
from datetime import datetime, timezone
from src.infrastructure.mappers.context.m_period import PeriodMapper
from src.infrastructure.orm.context.orm_period import PeriodORM
from src.domain.models.context.ve_period import Period
from src.domain.models.common.v_common import UUID, DateTime

def make_period_orm():
    return PeriodORM(
        id=uuid.uuid4(),
        name="19th Bundestag",
        start_date=datetime(2017, 10, 24, tzinfo=timezone.utc),
        end_date=datetime(2021, 10, 26, tzinfo=timezone.utc),
        description="19th legislative period of the Bundestag"
    )

def make_domain_entity():
    return Period(
        id=UUID(str(uuid.uuid4())),
        start_date=DateTime(datetime(2017, 10, 24, tzinfo=timezone.utc)),
        end_date=DateTime(datetime(2021, 10, 26, tzinfo=timezone.utc)),
        label="19th Bundestag",
        description="19th legislative period of the Bundestag"
    )

class TestPeriodMapper(unittest.TestCase):
    def test_period_orm_to_domain_conversion(self):
        # Direct test: known ORM -> expected domain
        orm_entity = PeriodORM(
            id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
            name="19th Bundestag",
            start_date=datetime(2017, 10, 24, tzinfo=timezone.utc),
            end_date=datetime(2021, 10, 26, tzinfo=timezone.utc),
            description="19th legislative period of the Bundestag"
        )
        expected_domain = Period(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            start_date=DateTime(datetime(2017, 10, 24, tzinfo=timezone.utc)),
            end_date=DateTime(datetime(2021, 10, 26, tzinfo=timezone.utc)),
            label="19th Bundestag",
            description="19th legislative period of the Bundestag"
        )
        domain_entity = PeriodMapper.to_domain(orm_entity)
        self.assertEqual(domain_entity.id, expected_domain.id)
        self.assertEqual(domain_entity.label, expected_domain.label)
        self.assertEqual(domain_entity.start_date, expected_domain.start_date)
        self.assertEqual(domain_entity.end_date, expected_domain.end_date)
        self.assertEqual(domain_entity.description, expected_domain.description)

    def test_period_domain_to_orm_conversion(self):
        # Direct test: known domain -> expected ORM
        domain_entity = Period(
            id=UUID("87654321-4321-8765-4321-876543218765"),
            start_date=DateTime(datetime(2015, 1, 1, tzinfo=timezone.utc)),
            end_date=DateTime(datetime(2019, 12, 31, tzinfo=timezone.utc)),
            label="18th Bundestag",
            description="18th legislative period of the Bundestag"
        )
        expected_orm = PeriodORM(
            id=uuid.UUID("87654321-4321-8765-4321-876543218765"),
            name="18th Bundestag",
            start_date=datetime(2015, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2019, 12, 31, tzinfo=timezone.utc),
            description="18th legislative period of the Bundestag"
        )
        orm_entity = PeriodMapper.to_orm(domain_entity)
        self.assertEqual(orm_entity.id, expected_orm.id)
        self.assertEqual(orm_entity.name, expected_orm.name)
        self.assertEqual(orm_entity.start_date, expected_orm.start_date)
        self.assertEqual(orm_entity.end_date, expected_orm.end_date)
        self.assertEqual(orm_entity.description, expected_orm.description)

    def test_period_mapper_back_and_forth(self):
        # Domain -> ORM -> Domain
        original_domain = make_domain_entity()
        orm_entity = PeriodMapper.to_orm(original_domain)
        mapped_domain = PeriodMapper.to_domain(orm_entity)
        self.assertEqual(original_domain.id.value, mapped_domain.id.value)
        self.assertEqual(original_domain.label, mapped_domain.label)
        self.assertEqual(original_domain.start_date.value, mapped_domain.start_date.value)
        self.assertEqual(original_domain.end_date.value, mapped_domain.end_date.value)
        self.assertEqual(original_domain.description, mapped_domain.description)

        # ORM -> Domain -> ORM
        original_orm = make_period_orm()
        domain_entity = PeriodMapper.to_domain(original_orm)
        mapped_orm = PeriodMapper.to_orm(domain_entity)
        self.assertEqual(original_orm.id, mapped_orm.id)
        self.assertEqual(original_orm.name, mapped_orm.name)
        self.assertEqual(original_orm.start_date, mapped_orm.start_date)
        self.assertEqual(original_orm.end_date, mapped_orm.end_date)
        self.assertEqual(original_orm.description, mapped_orm.description)

if __name__ == '__main__':
    unittest.main()


