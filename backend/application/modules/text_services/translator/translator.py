from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_text_translated import TranslatedText
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from backend.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_translated import TranslatedTextRepository
from backend.application.modules.text_services.translator.translator_spec import TranslatorSpec
from backend.domain.services.text.translator.serv_translator_dto import TranslatedTextDTO


class PreprocessTextService:
    def __init__(self, spec: TranslatorSpec):
        self.spec = spec
        self.speech_repo = SpeechRepository()
        self.speech_text_repo = SpeechTextRepository()
        self.clean_text_repo = CleanTextRepository()
        self.translated_text_repo = TranslatedTextRepository()

    def execute(self) -> TranslatedText:
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
        # 4. Get Translator
        translator_cls = TranslateCleanText()
        # 5. Translate
        service = TranslateCleanText(clean_text)
        translation_dto: TranslatedTextDTO = service.process()
        translated_text = TranslatedText(
            id=UUID.new(), speech_text_id=speech_text.id, translated_text=translation_dto.translation
        )
        self.translated_text_repo.add(translated_text)
        # 5. Update SpeechText with CleanText id
        speech_text.translated_text = translated_text.id
        self.speech_text_repo.update(speech_text)
        return translated_text
