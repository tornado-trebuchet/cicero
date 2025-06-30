from src.domain.models.text.e_protocol import Protocol
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.domain.models.common.v_enums import ProtocolTypeEnum, ExtensionEnum
from infrastructure.orm.text.orm_protocol import ProtocolORM
from src.domain.models.context.ve_period import Period
from src.infrastructure.mappers.context.m_period import PeriodMapper

class ProtocolMapper:
    
    @staticmethod
    def to_orm(domain_entity: Protocol) -> ProtocolORM:
        return ProtocolORM(
            id=domain_entity.id.value,
            institution_id=domain_entity.institution_id.value,
            period_id=domain_entity.period.id if domain_entity.period else None,
            extension=domain_entity.extension,
            protocol_text=domain_entity.protocol_text,
            file_source=str(domain_entity.file_source) if domain_entity.file_source else None,
            protocol_type=domain_entity.protocol_type,
            date=domain_entity.date.value,
            metadata_data=domain_entity.metadata
        )
    
    @staticmethod
    def to_domain(orm_entity: ProtocolORM) -> Protocol:
        period = None
        if orm_entity.period is not None:
            period = PeriodMapper.to_domain(orm_entity.period)
        # FIXME: ProtocolORM does not have a protocol_text field. This mapping is incomplete.
        return Protocol(
            id=UUID(str(orm_entity.id)),
            institution_id=UUID(str(orm_entity.institution_id)),
            period=period,
            extension=ExtensionEnum(orm_entity.extension),
            protocol_text=ProtocolText(),  # FIXME: protocol_text missing from ORM
            file_source=HttpUrl(orm_entity.file_source) if orm_entity.file_source else None,
            protocol_type=ProtocolTypeEnum(orm_entity.protocol_type),
            date=DateTime(orm_entity.date),
            metadata=orm_entity.metadata_data
        )