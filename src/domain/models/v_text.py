from typing import List
from src.domain.models.v_enums import LanguageEnum

class TextVO:
    """Value Object for speech text and its linguistic features."""
    def __init__(
        self,
        language_code: LanguageEnum,
        raw_text: str,
        clean_text: str,
        tokens: List[str],
        ngram_tokens: List[str],
        word_count: int,
    ):
        self.language_code = language_code
        self.raw_text = raw_text
        self.clean_text = clean_text
        self.tokens = tokens
        self.ngram_tokens = ngram_tokens
        self.word_count = word_count
    
    
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, TextVO)
            and self.language_code == other.language_code
            and self.raw_text == other.raw_text
            and self.clean_text == other.clean_text
            and self.tokens == other.tokens
            and self.ngram_tokens == other.ngram_tokens
            and self.word_count == other.word_count
        )

    def __repr__(self) -> str:
        return (
            f"<TextVO lang={self.language_code} words={self.word_count}>"
        )
