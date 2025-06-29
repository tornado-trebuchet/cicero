from typing import Optional
from domain.models.text.e_protocol import Protocol
from domain.models.common.v_common import UUID, DateTime, HttpUrl
from domain.models.common.v_enums import ProtocolTypeEnum, ExtensionEnum
from infrastructure.orm.context.orm_protocol import ProtocolORM


class ProtocolMapper:
    
    @staticmethod
    def to_orm(domain_entity: Protocol) -> ProtocolORM:
        return ProtocolORM(
            id=domain_entity.id.value,
            institution_id=domain_entity.institution_id.value,
            period_id=domain_entity.period.value if domain_entity.period else None,
            extension=domain_entity.extension,
            file_source=str(domain_entity.file_source) if domain_entity.file_source else None,
            protocol_type=domain_entity.protocol_type,
            regex_pattern_id=domain_entity.speech_regex.value if domain_entity.speech_regex else None,
            date=domain_entity.date.value,
            metadata_data=domain_entity.metadata
        )
    
    @staticmethod
    def to_domain(orm_entity: ProtocolORM) -> Protocol:
        return Protocol(
            id=UUID(str(orm_entity.id)),
            institution_id=UUID(str(orm_entity.institution_id)),
            period=UUID(str(orm_entity.period_id)) if orm_entity.period_id else None,
            extension=ExtensionEnum(orm_entity.extension),
            file_source=HttpUrl(orm_entity.file_source) if orm_entity.file_source else None,
            protocol_type=ProtocolTypeEnum(orm_entity.protocol_type),
            speech_regex=UUID(str(orm_entity.regex_pattern_id)) if orm_entity.regex_pattern_id else None,
            date=DateTime(orm_entity.date),
            metadata=orm_entity.metadata_data
        )