from typing import Optional

from src.domain.models.base_aggregate import AggregateRoot
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.v_text_metrics import TextMetrics


class SpeechText(AggregateRoot):
    """A collection of textual data for a speech"""

    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        raw_text: UUID,
        language_code: LanguageEnum,
        clean_text: Optional[UUID] = None,
        translated_text: Optional[UUID] = None,
        sentences: Optional[UUID] = None,
        tokens: Optional[UUID] = None,
        ngram_tokens: Optional[UUID] = None,
        text_metrics: Optional[TextMetrics] = None,
    ):
        super().__init__(id)
        self._speech_id = speech_id
        self._language_code = language_code
        self._raw_text = raw_text
        self._clean_text = clean_text
        self._translated_text = translated_text
        self._tokens = tokens
        self._sentences = sentences
        self._ngram_tokens = ngram_tokens
        self._text_metrics = text_metrics

    @property
    def speech_id(self) -> UUID:
        return self._speech_id

    @speech_id.setter
    def speech_id(self, value: UUID):
        self._speech_id = value

    @property
    def language_code(self) -> LanguageEnum:
        return self._language_code

    @language_code.setter
    def language_code(self, value: LanguageEnum):
        self._language_code = value

    @property
    def raw_text(self) -> UUID:
        return self._raw_text

    @raw_text.setter
    def raw_text(self, value: UUID):
        self._raw_text = value

    @property
    def clean_text(self) -> Optional[UUID]:
        return self._clean_text

    @clean_text.setter
    def clean_text(self, value: UUID):
        self._clean_text = value

    @property
    def translated_text(self) -> Optional[UUID]:
        return self._translated_text

    @translated_text.setter
    def translated_text(self, value: UUID):
        self._translated_text = value

    @property
    def tokens(self) -> Optional[UUID]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: UUID):
        self._tokens = value

    @property
    def sentences(self) -> Optional[UUID]:
        return self._sentences

    @sentences.setter
    def sentences(self, value: UUID):
        self._sentences = value

    @property
    def ngram_tokens(self) -> Optional[UUID]:
        return self._ngram_tokens

    @ngram_tokens.setter
    def ngram_tokens(self, value: UUID):
        self._ngram_tokens = value

    @property
    def text_metrics(self) -> Optional[TextMetrics]:
        return self._text_metrics

    @text_metrics.setter
    def text_metrics(self, value: TextMetrics):
        self._text_metrics = value

    def __repr__(self) -> str:
        return f"<TextVO lang={self._language_code} words={self._text_metrics}>"
