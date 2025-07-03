from typing import Optional, cast
from src.domain.models.context.e_party import Party
from src.domain.models.context.v_label import Label
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import PartyEnumRegistry, CountryEnum, GermanyPartyEnum
from src.infrastructure.orm.context.orm_party import PartyORM

# TODO: Move to country mapper for clarity use as private methots mb?
class PartyMapper:
    """Mapper for converting between Party domain entity and PartyORM."""
    
    @staticmethod
    def to_orm(domain_entity: Party) -> PartyORM:
        """Convert Party domain entity to ORM entity."""
        return PartyORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            label=domain_entity.label.value,
            party_enum_value=str(domain_entity.party_enum),  # Store enum value as string
            party_program=domain_entity.party_program
        )
    
    @staticmethod
    def to_domain(orm_entity: PartyORM) -> Party:
        """Convert PartyORM to Party domain entity.
        
        Note: This mapper cannot fully reconstruct Party because:
        1. party_enum requires country context and proper enum reconstruction
        2. members collection is not loaded here
        The repository layer should handle complete reconstruction.
        """
        # TODO: Repository should provide proper party enum reconstruction with country context
        # FIXME: Domain model type annotation is wrong - should accept enum instances, not PartyEnumRegistry
        placeholder_party_enum = cast(PartyEnumRegistry, GermanyPartyEnum.CDU)  # Placeholder - repository should handle this
        
        return Party(
            id=UUID(str(orm_entity.id)),
            country_id=UUID(str(orm_entity.country_id)),
            label=Label(orm_entity.label),
            party_enum=placeholder_party_enum,  # Domain model type annotation is incorrect
            members=[],  # Empty - repository should populate if needed
            party_program=orm_entity.party_program
        )
