from backend.domain.models.common.v_common import UUID, DateTime
from backend.domain.models.common.v_enums import GenderEnum
from backend.domain.models.context.e_speaker import Speaker
from backend.domain.models.context.v_name import Name
from backend.infrastructure.orm.context.orm_speaker import SpeakerORM


class SpeakerMapper:
    @staticmethod
    def to_orm(domain_entity: Speaker) -> SpeakerORM:
        orm = SpeakerORM(
            id=domain_entity.id.value,
            country_id=domain_entity.country_id.value,
            name=domain_entity.name.value,
            party_id=(domain_entity.party.value if domain_entity.party else None),
            role=domain_entity.role,
            birth_date=(domain_entity.birth_date.value if domain_entity.birth_date else None),
            gender=domain_entity.gender if domain_entity.gender else None,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SpeakerORM) -> Speaker:
        return Speaker(
            id=UUID(orm_entity.id),
            country_id=UUID(orm_entity.country_id),
            name=Name(orm_entity.name),
            speeches=(
                [UUID(s.id) for s in getattr(orm_entity, "speeches")]
                if hasattr(orm_entity, "speeches")
                else None
            ),
            party=UUID(orm_entity.party_id) if orm_entity.party_id else None,
            role=orm_entity.role,
            birth_date=(DateTime(orm_entity.birth_date) if orm_entity.birth_date else None),
            gender=(GenderEnum(orm_entity.gender) if orm_entity.gender else None),
        )
