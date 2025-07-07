from src.domain.models.text.e_text_ngrams import NGramizedText
from src.domain.models.common.v_common import UUID
from src.infrastructure.orm.text.orm_text_ngrams import TextNgramsORM

class NGramizedTextMapper:
    @staticmethod
    def to_orm(domain_entity: NGramizedText) -> TextNgramsORM:
        orm = TextNgramsORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_id.value,
            ngram_tokens=domain_entity.tokens
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: TextNgramsORM) -> NGramizedText:
        return NGramizedText(
            id=UUID(orm_entity.id),
            speech_id=UUID(orm_entity.speech_text_id),
            tokens=orm_entity.ngram_tokens
        )
