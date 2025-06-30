from src.domain.models.context.ve_speaker import Speaker
from src.domain.models.common.v_common import UUID
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
        # Note: Party enum reconstruction is complex and should be handled by repository
        # when it has knowledge of the country context
        # For now, we pass None for party - repository layer should handle party enum conversion
        
        return Speaker(
            id=UUID(str(orm_entity.id)),
            name=orm_entity.name,
            party=None,  # Repository layer will handle party enum conversion with country context
            role=orm_entity.role,
            birth_date=orm_entity.birth_date,
            gender=GenderEnum(orm_entity.gender) if orm_entity.gender else None
        )