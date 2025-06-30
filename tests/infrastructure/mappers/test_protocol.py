# import unittest
# import uuid
# from datetime import datetime, timezone
# from src.infrastructure.mappers.context.m_protocol import ProtocolMapper
# from src.infrastructure.orm.context.orm_protocol import ProtocolORM
# from src.domain.models.text.e_protocol import Protocol
# from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
# from src.domain.models.common.v_enums import ProtocolTypeEnum, ExtensionEnum

# def make_protocol_orm():
#     return ProtocolORM(
#         id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
#         institution_id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
#         period_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
#         extension=ExtensionEnum.XML.value,
#         file_source="https://example.com/protocol.xml",
#         protocol_type=ProtocolTypeEnum.PLENARY.value,
#         regex_pattern_id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
#         date=datetime(2020, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
#         metadata_data={"foo": "bar"}
#     )

# def make_domain_entity():
#     return Protocol(
#         id=UUID("11111111-1111-1111-1111-111111111111"),
#         institution_id=UUID("22222222-2222-2222-2222-222222222222"),
#         period=UUID("33333333-3333-3333-3333-333333333333"),
#         extension=ExtensionEnum.XML,
#         file_source=HttpUrl("https://example.com/protocol.xml"),
#         protocol_type=ProtocolTypeEnum.PLENARY,
#         date=DateTime(datetime(2020, 1, 1, 10, 0, 0, tzinfo=timezone.utc)),
#         metadata={"foo": "bar"}
#     )

# class TestProtocolMapper(unittest.TestCase):
#     def test_protocol_orm_to_domain_conversion(self):
#         orm_entity = make_protocol_orm()
#         expected_domain = make_domain_entity()
#         domain_entity = ProtocolMapper.to_domain(orm_entity)
#         self.assertEqual(domain_entity.id, expected_domain.id)
#         self.assertEqual(domain_entity.institution_id, expected_domain.institution_id)
#         self.assertEqual(domain_entity.period, expected_domain.period)
#         self.assertEqual(domain_entity.extension, expected_domain.extension)
#         self.assertEqual(domain_entity.file_source, expected_domain.file_source)
#         self.assertEqual(domain_entity.protocol_type, expected_domain.protocol_type)
#         self.assertEqual(domain_entity.date, expected_domain.date)
#         self.assertEqual(domain_entity.metadata, expected_domain.metadata)

#     def test_protocol_domain_to_orm_conversion(self):
#         domain_entity = make_domain_entity()
#         expected_orm = make_protocol_orm()
#         orm_entity = ProtocolMapper.to_orm(domain_entity)
#         self.assertEqual(orm_entity.id, expected_orm.id)
#         self.assertEqual(orm_entity.institution_id, expected_orm.institution_id)
#         self.assertEqual(orm_entity.period_id, expected_orm.period_id)
#         self.assertEqual(orm_entity.extension, expected_orm.extension)
#         self.assertEqual(orm_entity.file_source, expected_orm.file_source)
#         self.assertEqual(orm_entity.protocol_type, expected_orm.protocol_type)
#         self.assertEqual(orm_entity.date, expected_orm.date)
#         self.assertEqual(orm_entity.metadata_data, expected_orm.metadata_data)

#     def test_protocol_mapper_back_and_forth(self):
#         # Domain -> ORM -> Domain
#         original_domain = make_domain_entity()
#         orm_entity = ProtocolMapper.to_orm(original_domain)
#         mapped_domain = ProtocolMapper.to_domain(orm_entity)
#         self.assertEqual(original_domain.id, mapped_domain.id)
#         self.assertEqual(original_domain.institution_id, mapped_domain.institution_id)
#         self.assertEqual(original_domain.period, mapped_domain.period)
#         self.assertEqual(original_domain.extension, mapped_domain.extension)
#         self.assertEqual(original_domain.file_source, mapped_domain.file_source)
#         self.assertEqual(original_domain.protocol_type, mapped_domain.protocol_type)
#         self.assertEqual(original_domain.date, mapped_domain.date)
#         self.assertEqual(original_domain.metadata, mapped_domain.metadata)

#         # ORM -> Domain -> ORM
#         original_orm = make_protocol_orm()
#         domain_entity = ProtocolMapper.to_domain(original_orm)
#         mapped_orm = ProtocolMapper.to_orm(domain_entity)
#         self.assertEqual(original_orm.id, mapped_orm.id)
#         self.assertEqual(original_orm.institution_id, mapped_orm.institution_id)
#         self.assertEqual(original_orm.period_id, mapped_orm.period_id)
#         self.assertEqual(original_orm.extension, mapped_orm.extension)
#         self.assertEqual(original_orm.file_source, mapped_orm.file_source)
#         self.assertEqual(original_orm.protocol_type, mapped_orm.protocol_type)
#         self.assertEqual(original_orm.date, mapped_orm.date)
#         self.assertEqual(original_orm.metadata_data, mapped_orm.metadata_data)

# if __name__ == '__main__':
#     unittest.main()


