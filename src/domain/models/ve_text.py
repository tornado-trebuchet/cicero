from typing import List, Optional
from src.domain.models.v_enums import LanguageEnum
from src.domain.models.v_common import UUID
from src.domain.models.base_model import Entity

class Text(Entity):
    """Value Object (very special, proud and mutable VO) for speech text and its linguistic features."""
    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        raw_text: str,
        language_code: Optional[LanguageEnum] = None,
        clean_text: Optional[str] = None,
        tokens: Optional[List[str]] = None,
        ngram_tokens: Optional[List[str]] = None,
        word_count: Optional[int] = None,
    ):
        super().__init__(id)
        self._speech_id = speech_id
        self._language_code = language_code
        self._raw_text = raw_text
        self._clean_text = clean_text if clean_text is not None else ""
        self._tokens = tokens if tokens is not None else []
        self._ngram_tokens = ngram_tokens if ngram_tokens is not None else []
        self._word_count = word_count if word_count is not None else 0

    @property
    def speech_id(self) -> UUID:
        return self._speech_id

    @speech_id.setter
    def speech_id(self, value: UUID):
        self._speech_id = value

    @property
    def language_code(self) -> Optional[LanguageEnum]:
        return self._language_code

    @language_code.setter
    def language_code(self, value: Optional[LanguageEnum]):
        self._language_code = value

    @property
    def raw_text(self) -> str:
        return self._raw_text

    @raw_text.setter
    def raw_text(self, value: str):
        self._raw_text = value

    @property
    def clean_text(self) -> str:
        return self._clean_text

    @clean_text.setter
    def clean_text(self, value: str):
        self._clean_text = value

    @property
    def tokens(self) -> list[str]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: list[str]):
        self._tokens = value

    @property
    def ngram_tokens(self) -> list[str]:
        return self._ngram_tokens

    @ngram_tokens.setter
    def ngram_tokens(self, value: list[str]):
        self._ngram_tokens = value

    @property
    def word_count(self) -> int:
        return self._word_count

    @word_count.setter
    def word_count(self, value: int):
        self._word_count = value

    def __repr__(self) -> str:
        return f"<TextVO lang={self._language_code} words={self._word_count}>"
