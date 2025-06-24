from typing import Optional, List
from src.domain.models.ve_text import Text
from src.domain.models.v_common import UUID
from src.domain.models.v_enums import LanguageEnum
from src.infrastructure.orm.orm_text import TextORM


class TextMapper:
    """Mapper for Text entity and TextORM."""
    
    @staticmethod
    def to_orm(domain_entity: Text) -> TextORM:
        """Convert Text domain entity to TextORM."""
        return TextORM(
            id=domain_entity.id.value,
            speech_id=domain_entity.speech_id.value,
            language_code=domain_entity.language_code,
            raw_text=domain_entity.raw_text,
            clean_text=domain_entity.clean_text,
            tokens=domain_entity.tokens,
            ngram_tokens=domain_entity.ngram_tokens,
            word_count=domain_entity.word_count
        )
    
    @staticmethod
    def to_domain(orm_entity: TextORM) -> Text:
        """Convert TextORM to Text domain entity."""
        return Text(
            id=UUID(str(orm_entity.id)),
            speech_id=UUID(str(orm_entity.speech_id)),
            raw_text=orm_entity.raw_text,
            language_code=LanguageEnum(orm_entity.language_code) if orm_entity.language_code else None,
            clean_text=orm_entity.clean_text,
            tokens=orm_entity.tokens or [],
            ngram_tokens=orm_entity.ngram_tokens or [],
            word_count=orm_entity.word_count or 0
        )
