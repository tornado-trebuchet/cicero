from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_text_split import TextSentences
from backend.infrastructure.orm.text.orm_text_split import SplitTextORM


class TextSentencesMapper:
    @staticmethod
    def to_orm(domain_entity: TextSentences) -> SplitTextORM:
        orm = SplitTextORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_text_id.value,
            sentences=domain_entity.sentences,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: SplitTextORM) -> TextSentences:
        return TextSentences(
            id=UUID(orm_entity.id),
            speech_text_id=UUID(orm_entity.speech_text_id),
            sentences=orm_entity.sentences,
        )
