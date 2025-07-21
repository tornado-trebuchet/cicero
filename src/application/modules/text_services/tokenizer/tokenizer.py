from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_tokenized import TokenizedText
from src.domain.services.text.tokenizer.serv_tokenizer import TokenizeCleanText
from src.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from src.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
from src.application.modules.text_services.tokenizer.tokenizer_spec import TokenizerSpec

class PreprocessTextService:
    def __init__(self, spec: TokenizerSpec):
        self.spec = spec
        self.speech_repo = SpeechRepository()
        self.speech_text_repo = SpeechTextRepository()
        self.clean_text_repo = CleanTextRepository()
        self.tokenized_text_repo = TokenizedTextRepository()

    def execute(self) -> TokenizedText:
        # 1. Get Speech
        speech = self.speech_repo.get_by_id(self.spec.speech)
        if speech is None:
            raise ValueError(f"No Speech found for id: {self.spec.speech}")
        # 2. Get SpeechText
        speech_text = self.speech_text_repo.get_by_id(speech.text)
        if speech_text is None:
            raise ValueError(f"No SpeechText found for id: {speech.text}")
        # 3. Get CleanText
        clean_text = self.clean_text_repo.get_by_id(speech_text.raw_text)
        if clean_text is None:
            raise ValueError(f"No CleanText found for id: {speech_text.raw_text}")
        # 4. Get Tokenizer and Stopwords 
        language_code = speech_text.language_code
        tokenizer_cls = TokenizeCleanText.pick_tokenizer(language_code)
        if tokenizer_cls is None:
            raise ValueError(f"No tokenizerr found for language: {language_code}")
        stopwords_cls = TokenizeCleanText.pick_stopwords(language_code)
        if stopwords_cls is None:
            raise ValueError(f"No stopwords found for language: {language_code}")
        # 5. Tokenize
        service = TokenizeCleanText(clean_text, language_code)
        tokens_dto = service.process(tokenizer_cls, stopwords_cls().get_stopwords())
        tokenized_text = TokenizedText(
            id=UUID.new(),
            speech_text_id=speech_text.id,
            tokens=tokens_dto.tokens
        )
        self.tokenized_text_repo.add(tokenized_text)
        # 5. Update SpeechText with CleanText id
        speech_text.tokenized_text = tokenized_text.id
        self.speech_text_repo.update(speech_text)
        return tokenized_text