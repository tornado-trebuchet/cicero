from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_text_clean import CleanText
from backend.infrastructure.orm.text.orm_text_clean import CleanTextORM


class CleanTextMapper:
    @staticmethod
    def to_orm(domain_entity: CleanText) -> CleanTextORM:
        orm = CleanTextORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_text_id.value,
            clean_text=domain_entity.text,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: CleanTextORM) -> CleanText:
        return CleanText(
            id=UUID(orm_entity.id),
            speech_text_id=UUID(orm_entity.speech_text_id),
            text=orm_entity.clean_text,
        )
