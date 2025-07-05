from typing import Optional
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.common.v_common import UUID
from src.domain.models.base_model import Entity
from src.domain.models.text.v_text_metrics import TextMetrics   
from src.domain.models.text.v_text_raw import RawText
from src.domain.models.text.v_text_clean import CleanText
from src.domain.models.text.v_text_tokenized import TokenizedText
from src.domain.models.text.v_text_ngrams import NGramizedText
from src.domain.models.text.v_speech_sentences import SpeechSentences
from src.domain.models.text.v_text_translated import TranslatedText


# FIXME: this is very heavy. If a processor needs a part of it to load, there is an astronomical overhead. 
class SpeechText(Entity):
    """
    Value Object (very special, proud and mutable and holding multiple subservants VO) 
    for speech text and its linguistic features.
    """
    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        raw_text: RawText,
        language_code: LanguageEnum,
        clean_text: Optional[CleanText] = None,
        translated_text: Optional[TranslatedText] = None,
        tokens: Optional[TokenizedText] = None,
        sentences: Optional[SpeechSentences] = None,
        ngram_tokens: Optional[NGramizedText] = None,
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
    def tokens(self) -> Optional[TokenizedText]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: TokenizedText):
        self._tokens = value

    @property
    def sentences(self) -> Optional[SpeechSentences]:
        return self._sentences
    
    @sentences.setter
    def sentences(self, value: SpeechSentences):
        self._sentences = value

    @property
    def ngram_tokens(self) -> Optional[NGramizedText]:
        return self._ngram_tokens

    @ngram_tokens.setter
    def ngram_tokens(self, value: NGramizedText):
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
