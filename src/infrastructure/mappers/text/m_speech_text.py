from typing import Optional, List
from domain.models.text.a_speech_text import SpeechText
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import LanguageEnum
from domain.models.text.e_text_raw import RawText
from domain.models.text.e_text_clean import CleanText
from domain.models.text.e_text_tokenized import TokenizedText
from domain.models.text.e_text_ngrams import NGramizedText
from src.infrastructure.orm.text.orm_speech_text import TextORM

# TODO:  definitely needs a way to load partially with elegance 
class TextMapper:
    """Mapper for SpeechText entity and TextORM."""
    
    @staticmethod
    def to_orm(domain_entity: SpeechText) -> TextORM:
        """Convert SpeechText domain entity to TextORM."""
        return TextORM(
            id=domain_entity.id.value,
            speech_id=domain_entity.speech_id.value,
            language_code=domain_entity.language_code,
            raw_text=domain_entity.raw_text.text if domain_entity.raw_text else None,
            clean_text=domain_entity.clean_text.text if domain_entity.clean_text else None,
            tokens=domain_entity.tokens.tokens if domain_entity.tokens else None,
            ngram_tokens=domain_entity.ngram_tokens.tokens if domain_entity.ngram_tokens else None
        )
    
    @staticmethod
    def to_domain(orm_entity: TextORM) -> SpeechText:
        """Convert TextORM to SpeechText domain entity."""
        return SpeechText(
            id=UUID(str(orm_entity.id)),
            speech_id=UUID(str(orm_entity.speech_id)),
            raw_text=RawText(orm_entity.raw_text) if orm_entity.raw_text else RawText(""),
            language_code=LanguageEnum(orm_entity.language_code) if orm_entity.language_code else LanguageEnum.EN,
            clean_text=CleanText(orm_entity.clean_text) if orm_entity.clean_text else None,
            tokens=TokenizedText(orm_entity.tokens) if orm_entity.tokens else None,
            ngram_tokens=NGramizedText(orm_entity.ngram_tokens) if orm_entity.ngram_tokens else None
        )
