from domain.models.context.e_institution import Institution
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import InstitutionTypeEnum
from domain.models.common.ve_metadata_plugin import MetadataPlugin
from infrastructure.orm.context.orm_institution import InstitutionORM


class InstitutionMapper:
    
    @staticmethod
    def to_orm(domain_entity: Institution) -> InstitutionORM:
        return InstitutionORM(
            id=domain_entity.id.value,
            country_id=domain_entity.state_id.value,  
            institution_type=domain_entity.institution_type,
            metadata_data=domain_entity.metadata._data if domain_entity.metadata else {}
        )
    
    @staticmethod
    def to_domain(orm_entity: InstitutionORM) -> Institution:
        # Note: Not loading periods here to avoid circular dependencies
        # Periods should be loaded separately by repository if needed
        metadata_data = getattr(orm_entity, 'metadata_data', {}) or {}
        
        return Institution(
            id=UUID(str(orm_entity.id)),
            state_id=UUID(str(orm_entity.country_id)),  # Map back to state_id for domain
            institution_type=InstitutionTypeEnum(orm_entity.institution_type),
            periodisation=[],  # Load separately if needed
            metadata=MetadataPlugin(metadata_data)
        )

