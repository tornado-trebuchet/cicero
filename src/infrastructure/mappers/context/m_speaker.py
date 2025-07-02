from src.domain.models.context.e_speaker import Speaker
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.common.v_enums import GenderEnum
from src.infrastructure.orm.context.orm_speaker import SpeakerORM


class SpeakerMapper:
    
    @staticmethod
    def to_orm(domain_entity: Speaker) -> SpeakerORM:
        party_value = None
        if domain_entity.party:
            party_value = str(domain_entity.party)
        
        return SpeakerORM(
            id=domain_entity.id.value,
            name=domain_entity.name,
            party=party_value,
            role=domain_entity.role,
            birth_date=domain_entity.birth_date,
            gender=domain_entity.gender
        )
    
    @staticmethod
    def to_domain(orm_entity: SpeakerORM) -> Speaker:
        """Convert SpeakerORM to Speaker domain entity."""
        # Note: This mapper cannot fully reconstruct Speaker because:
        # 1. country_id is not available in SpeakerORM
        # 2. speeches collection is not loaded here
        # 3. party enum requires country context
        # The repository layer should handle complete reconstruction
        
        # For now, provide minimal reconstruction - repository should complete it
        from src.domain.models.common.v_common import UUID
        
        return Speaker(
            id=UUID(str(orm_entity.id)),
            country_id=UUID.new(),  # TODO: Repository should provide correct country_id
            name=orm_entity.name,
            speeches=[],  # TODO: Repository should load speeches if needed
            party=None,  # TODO: Repository should handle party enum conversion with country context
            role=orm_entity.role,
            birth_date=DateTime(orm_entity.birth_date.isoformat()) if orm_entity.birth_date else None,
            gender=GenderEnum(orm_entity.gender) if orm_entity.gender else None
        )