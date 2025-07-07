from src.domain.models.text.a_protocol import Protocol
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.domain.models.common.v_enums import ProtocolTypeEnum
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.text.v_protocol_agenda import Agenda
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.infrastructure.orm.text.orm_protocol import ProtocolORM

class ProtocolMapper:
    @staticmethod
    def to_orm(domain_entity: Protocol) -> ProtocolORM:
        orm = ProtocolORM(
            id=domain_entity.id.value,
            institution_id=domain_entity.institution_id.value,
            date=domain_entity.date.value,
            protocol_type=domain_entity.protocol_type.value,
            protocol_text=domain_entity.protocol_text.protocol_text,
            agenda=domain_entity.agenda.items if domain_entity.agenda is not None else None,
            file_source=domain_entity.file_source if domain_entity.file_source else None,
            metadata_data=domain_entity.metadata,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: ProtocolORM) -> Protocol:
        return Protocol(
            id=UUID(orm_entity.id),
            institution_id=UUID(orm_entity.institution_id),
            date=DateTime(orm_entity.date),
            protocol_type=ProtocolTypeEnum(orm_entity.protocol_type),
            protocol_text=ProtocolText(orm_entity.protocol_text),
            agenda=Agenda(orm_entity.agenda) if orm_entity.agenda else None,
            file_source=HttpUrl(orm_entity.file_source) if orm_entity.file_source else None,
            protocol_speeches=[UUID(s.id) for s in getattr(orm_entity, 'speeches')] if hasattr(orm_entity, 'speeches') else None,
            metadata=MetadataPlugin(orm_entity.metadata_data) if orm_entity.metadata_data else None,
        )
