from src.domain.models.common.v_common import UUID
from src.domain.models.context.e_institution import Institution
from src.infrastructure.orm.context.orm_institution import InstitutionORM
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.domain.models.context.v_label import Label

class InstitutionMapper:
    @staticmethod
    def to_orm(domain_entity: Institution) -> InstitutionORM:
        orm = InstitutionORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            institution_type=domain_entity.type,
            label=domain_entity.label.value,
            meta_data=domain_entity.metadata.get_properties() if domain_entity.metadata else None
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: InstitutionORM) -> Institution:
        periodisation = getattr(orm_entity, 'periods', None)
        protocols = getattr(orm_entity, 'protocols', None)
        return Institution(
            id=UUID(orm_entity.id),
            country_id=UUID(orm_entity.country_id),
            type=InstitutionTypeEnum(orm_entity.institution_type),
            label=Label(orm_entity.label),
            protocols=[UUID(p.id) for p in protocols] if protocols else None,
            periodisation=[UUID(p.id) for p in periodisation] if periodisation else None,
            metadata= MetadataPlugin(orm_entity.meta_data) if orm_entity.meta_data else None
        )
