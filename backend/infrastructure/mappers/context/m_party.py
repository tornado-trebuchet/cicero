from backend.domain.models.common.v_common import UUID
from backend.domain.models.context.e_party import Party
from backend.domain.models.context.v_party_name import PartyName
from backend.domain.models.text.v_party_program_text import PartyProgramText
from backend.infrastructure.orm.context.orm_party import PartyORM


class PartyMapper:
    @staticmethod
    def to_orm(domain_entity: Party) -> PartyORM:
        orm = PartyORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            label=domain_entity.party_name.value,
            party_enum_value=domain_entity.party_name.value,
            party_program=(domain_entity.party_program.program_text if domain_entity.party_program else None),
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: PartyORM) -> Party:
        return Party(
            id=UUID(orm_entity.id),
            country_id=UUID(orm_entity.country_id),
            party_name=PartyName(orm_entity.label),
            party_program=(PartyProgramText(orm_entity.party_program) if orm_entity.party_program else None),
            speakers=(
                [UUID(s.id) for s in getattr(orm_entity, "members")]
                if hasattr(orm_entity, "members")
                else None
            ),
        )
