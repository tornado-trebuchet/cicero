from src.domain.models.text.a_protocol import Protocol
from src.domain.models.text.v_protocol_text import ProtocolText
from src.domain.models.common.v_common import UUID, DateTime, HttpUrl
from src.domain.models.common.v_enums import ProtocolTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.infrastructure.orm.text.orm_protocol import ProtocolORM

class ProtocolMapper:
    
    @staticmethod
    def to_orm(domain_entity: Protocol) -> ProtocolORM:
        # Period is a ValueObject, so we don't store period_id in Protocol table
        # The relationship is maintained differently or may not be needed
        return ProtocolORM(
            id=domain_entity.id.value,
            institution_id=domain_entity.institution_id.value,
            period_id=None,  # Period is ValueObject, no separate table reference
            file_source=str(domain_entity.file_source) if domain_entity.file_source else None,
            protocol_type=domain_entity.protocol_type,
            date=domain_entity.date.value,
            metadata_data=domain_entity.metadata._data if domain_entity.metadata else {}
        )
    
    @staticmethod
    def to_domain(orm_entity: ProtocolORM) -> Protocol:
        # Since Period is ValueObject, we might need to get it from elsewhere
        # For now, set to None - this needs domain clarification
        period = None
        if orm_entity.period is not None:
            period = PeriodMapper.to_domain(orm_entity.period)
        
        # Get country_id from institution relationship
        country_id = UUID(str(orm_entity.institution.country_id))
        
        return Protocol(
            id=UUID(str(orm_entity.id)),
            country_id=country_id,
            institution_id=UUID(str(orm_entity.institution_id)),
            period=period,
            protocol_text=ProtocolText(""),  # TODO: protocol_text missing from ORM
            file_source=HttpUrl(orm_entity.file_source) if orm_entity.file_source else None,
            protocol_type=ProtocolTypeEnum(orm_entity.protocol_type),
            date=DateTime(orm_entity.date),
            metadata=MetadataPlugin(orm_entity.metadata_data) if orm_entity.metadata_data else None
        )