from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_tokenized import TokenizedText
from src.infrastructure.orm.text.orm_text_tokenized import TokenizedTextORM


class TokenizedTextMapper:
    @staticmethod
    def to_orm(domain_entity: TokenizedText) -> TokenizedTextORM:
        orm = TokenizedTextORM(
            id=domain_entity.id.value,
            speech_text_id=domain_entity.speech_text_id.value,
            tokens=domain_entity.tokens,
        )
        return orm

    @staticmethod
    def to_domain(orm_entity: TokenizedTextORM) -> TokenizedText:
        return TokenizedText(
            id=UUID(orm_entity.id),
            speech_text_id=UUID(orm_entity.speech_text_id),
            tokens=orm_entity.tokens,
        )
