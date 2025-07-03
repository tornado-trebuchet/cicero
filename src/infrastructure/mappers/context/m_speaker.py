from typing import Optional
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.v_name import Name
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.common.v_enums import GenderEnum
from src.infrastructure.orm.context.orm_speaker import SpeakerORM

# TODO: Move to country mapper for clarity use as private methots mb?
class SpeakerMapper:
    """Mapper for converting between Speaker domain entity and SpeakerORM."""
    
    @staticmethod
    def to_orm(domain_entity: Speaker) -> SpeakerORM:
        """Convert Speaker domain entity to ORM entity."""
        # Handle party reference
        party_id = None
        if domain_entity.party:
            party_id = domain_entity.party.id.value
        
        return SpeakerORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            party_id=party_id,
            name=domain_entity.name.value,  # Convert Name value object to string
            role=domain_entity.role,
            birth_date=domain_entity.birth_date.value if domain_entity.birth_date else None,
            gender=domain_entity.gender
        )
    
    @staticmethod
    def to_domain(orm_entity: SpeakerORM) -> Speaker:
        """Convert SpeakerORM to Speaker domain entity.
        
        Note: This mapper cannot fully reconstruct Speaker because:
        1. speeches collection is not loaded here  
        2. party entity requires separate loading and enum reconstruction
        The repository layer should handle complete reconstruction.
        """
        return Speaker(
            id=UUID(str(orm_entity.id)),
            country_id=UUID(str(orm_entity.country_id)),
            name=Name(orm_entity.name),
            speeches=[],  # Empty - repository should load speeches if needed
            party=None,   # TODO: Repository should load party entity if party_id exists
            role=orm_entity.role,
            birth_date=DateTime(orm_entity.birth_date.isoformat()) if orm_entity.birth_date else None,
            gender=GenderEnum(orm_entity.gender) if orm_entity.gender else None
        )