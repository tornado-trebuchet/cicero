from src.domain.models.context.e_institution import Institution
from src.domain.models.context.v_period import Period
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.common.v_metadata_plugin import MetadataPlugin
from src.infrastructure.orm.context.orm_institution import InstitutionORM

# TODO: Move to country mapper for clarity use as private methots mb?
class InstitutionMapper:
    
    @staticmethod
    def to_orm(domain_entity: Institution) -> InstitutionORM:
        # Convert periods to JSON data
        periods_data = []
        for period in domain_entity.periodisation or []:
            periods_data.append({
                "label": period.label,
                "start_date": period.start_date.value.isoformat(),
                "end_date": period.end_date.value.isoformat(),
                "description": period.description
            })
        
        return InstitutionORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            institution_type=domain_entity.institution_type,
            periods_data=periods_data,
            metadata_data=domain_entity.metadata._data if domain_entity.metadata else {}
        )
    
    @staticmethod
    def to_domain(orm_entity: InstitutionORM) -> Institution:
        # Convert periods data back to Period ValueObjects
        periods = []
        for period_data in orm_entity.periods_data or []:
            period = Period(
                label=period_data.get("label"), # FIXME: this thing should be generated in domain from something at least initially
                start_date=DateTime(period_data["start_date"]),
                end_date=DateTime(period_data["end_date"]),
                description=period_data.get("description")
            )
            periods.append(period)
        
        metadata_data = getattr(orm_entity, 'metadata_data', {}) or {}
        
        return Institution(
            id=UUID(str(orm_entity.id)),
            country_id=UUID(str(orm_entity.country_id)),
            institution_type=InstitutionTypeEnum(orm_entity.institution_type),
            periodisation=periods,
            metadata=MetadataPlugin(metadata_data)
        )

