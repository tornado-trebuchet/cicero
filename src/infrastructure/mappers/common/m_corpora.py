from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.infrastructure.orm.common.orm_corpora import CorporaORM


class CorporaMapper:
    @staticmethod
    def to_orm(domain_entity: Corpora) -> CorporaORM:
        orm = CorporaORM(
            id=domain_entity.id.value,
            label=domain_entity.label.value,
            countries=([uuid.value for uuid in domain_entity.countries] if domain_entity.countries else None),
            institutions=(
                [uuid.value for uuid in domain_entity.institutions] if domain_entity.institutions else None
            ),
            periods=([uuid.value for uuid in domain_entity.periods] if domain_entity.periods else None),
            parties=([uuid.value for uuid in domain_entity.parties] if domain_entity.parties else None),
            speakers=([uuid.value for uuid in domain_entity.speakers] if domain_entity.speakers else None),
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: CorporaORM) -> Corpora:
        return Corpora(
            id=UUID(orm_entity.id),
            label=Label(orm_entity.label),
            texts=set(UUID(s.id) for s in getattr(orm_entity, "speeches")),
            countries=([UUID(cid) for cid in orm_entity.countries] if orm_entity.countries else None),
            institutions=(
                [UUID(iid) for iid in orm_entity.institutions] if orm_entity.institutions else None
            ),
            periods=([UUID(pid) for pid in orm_entity.periods] if orm_entity.periods else None),
            parties=([UUID(pid) for pid in orm_entity.parties] if orm_entity.parties else None),
            speakers=([UUID(sid) for sid in orm_entity.speakers] if orm_entity.speakers else None),
        )
