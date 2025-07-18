from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_translated import TranslatedText
from src.infrastructure.orm.text.orm_text_translated import TranslatedTextORM


class TranslatedTextMapper:
    @staticmethod
    def to_orm(domain_entity: TranslatedText) -> TranslatedTextORM:
        orm = TranslatedTextORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_id.value,
            translated_text=domain_entity.translation,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: TranslatedTextORM) -> TranslatedText:
        return TranslatedText(
            id=UUID(orm_entity.id),
            speech_id=UUID(orm_entity.speech_text_id),
            translated_text=orm_entity.translated_text,
        )
