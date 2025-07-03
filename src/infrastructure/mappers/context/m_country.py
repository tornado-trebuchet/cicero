from typing import Optional, List
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.infrastructure.orm.context.orm_country import CountryORM


class CountryMapper:
    """Mapper for converting between Country domain aggregate and CountryORM."""
    
    @staticmethod
    def to_orm(domain_entity: Country) -> CountryORM:
        """Convert Country domain aggregate to ORM entity.
        
        Note: This only converts the core Country data.
        Related entities (institutions, speakers, parties) are handled separately
        by their respective repositories to avoid circular dependencies.
        """
        return CountryORM(
            id=domain_entity.id.value,
            name=domain_entity.country
        )
    
    @staticmethod
    def to_domain(orm_entity: CountryORM) -> Country:
        """Convert CountryORM to Country domain entity with minimal data.
        
        Note: This creates a Country with empty relationship collections.
        The repository layer should use _rehydrate_country_aggregate for
        full aggregate reconstruction including all relationships.
        """
        return Country(
            id=UUID(str(orm_entity.id)),
            country=CountryEnum(orm_entity.name),
            institutions=[],  # Empty - repository should populate if needed
            speakers=[],      # Empty - repository should populate if needed  
            parties=[]        # Empty - repository should populate if needed
        )
    
    @staticmethod
    def to_domain_with_relationships(
        orm_entity: CountryORM,
        institutions: Optional[List[Institution]] = None,
        speakers: Optional[List[Speaker]] = None,
        parties: Optional[List[Party]] = None
    ) -> Country:
        """Convert CountryORM to Country domain aggregate with provided relationships.
        
        This method is used by the repository's _rehydrate_country_aggregate method
        to construct the full aggregate with all relationships properly loaded.
        """
        return Country(
            id=UUID(str(orm_entity.id)),
            country=CountryEnum(orm_entity.name),
            institutions=institutions or [],
            speakers=speakers or [],
            parties=parties or []
        )