from typing import Optional
from domain.models.common.v_enums import LanguageEnum
from domain.models.common.v_common import UUID
from domain.models.common.base_model import Entity
from domain.models.text.v_text_metrics import TextMetrics   
from domain.models.text.v_raw_text import RawText
from domain.models.text.v_clean_text import CleanText
from domain.models.text.v_tokenized_text import Tokens
from domain.models.text.v_ngram_tokens import NGramTokens
from domain.models.text.v_speech_sentences import SpeechSentences

class Text(Entity):
    """Value Object (very special, proud and mutable VO) for speech text and its linguistic features."""
    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        raw_text: RawText,
        language_code: LanguageEnum,
        clean_text: Optional[CleanText] = None,
        tokens: Optional[Tokens] = None,
        sentences: Optional[SpeechSentences] = None,
        ngram_tokens: Optional[NGramTokens] = None,
        text_metrics: Optional[TextMetrics] = None,
    ):
        super().__init__(id)
        self._speech_id = speech_id
        self._language_code = language_code
        self._raw_text = raw_text
        self._clean_text = clean_text if clean_text is not None else CleanText()
        self._tokens = tokens if tokens is not None else Tokens()
        self._sentences = sentences if sentences is not None else SpeechSentences()
        self._ngram_tokens = ngram_tokens if ngram_tokens is not None else NGramTokens()
        self._text_metrics = text_metrics if text_metrics is not None else None

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
    def raw_text(self) -> RawText:
        return self._raw_text

    @raw_text.setter
    def raw_text(self, value: RawText):
        self._raw_text = value

    @property
    def clean_text(self) -> Optional[CleanText]:
        return self._clean_text

    @clean_text.setter
    def clean_text(self, value: CleanText):
        self._clean_text = value

    @property
    def tokens(self) -> Optional[Tokens]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: Tokens):
        self._tokens = value

    @property
    def sentences(self) -> Optional[SpeechSentences]:
        return self._sentences
    
    @sentences.setter
    def sentences(self, value: SpeechSentences):
        self._sentences = value

    @property
    def ngram_tokens(self) -> Optional[NGramTokens]:
        return self._ngram_tokens

    @ngram_tokens.setter
    def ngram_tokens(self, value: NGramTokens):
        self._ngram_tokens = value

    @property
    def text_metrics(self) -> Optional[TextMetrics]:
        return self._text_metrics
    
    @text_metrics.setter
    def text_metrics(self, value: TextMetrics):
        self._text_metrics = value

    def split_sentences(self) -> SpeechSentences:
        """Splits the clean text into sentences."""
        if not self._clean_text:
            raise ValueError("Clean text is not set.")
        sentences = self._clean_text.split_sentences()
        self._sentences = SpeechSentences(sentences=sentences)
        return self._sentences


    def __repr__(self) -> str:
        return f"<TextVO lang={self._language_code} words={self._text_metrics}>"
