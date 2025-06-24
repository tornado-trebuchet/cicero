from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.models.v_common import UUID
from src.infrastructure.orm.orm_regex_pattern import RegexPatternORM


class RegexPatternMapper:
    
    @staticmethod
    def to_orm(domain_entity: RegexPattern) -> RegexPatternORM:
        return RegexPatternORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country.value,
            institution_id=domain_entity.institution.value,
            period_id=domain_entity.period.value if domain_entity.period else None,
            pattern=domain_entity.pattern,
            description=domain_entity.description,
            version=domain_entity.version if domain_entity.version else 1,
            is_active=domain_entity.is_active
        )
    
    @staticmethod
    def to_domain(orm_entity: RegexPatternORM) -> RegexPattern:
        return RegexPattern(
            id=UUID(str(orm_entity.id)),
            country=UUID(str(orm_entity.country_id)),
            institution=UUID(str(orm_entity.institution_id)),
            period=UUID(str(orm_entity.period_id)) if orm_entity.period_id else None,
            pattern=orm_entity.pattern,
            description=orm_entity.description,
            version=orm_entity.version,
            is_active=orm_entity.is_active
        )