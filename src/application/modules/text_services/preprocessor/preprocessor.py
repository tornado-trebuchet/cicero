from src.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from src.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from src.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from src.domain.models.text.e_text_clean import CleanText
from src.domain.models.common.v_common import UUID
from src.domain.services.text.preprocessor.serv_preprocessor import PreprocessRawText

# Here
class PreprocessTextService:
    def __init__(self, spec: PreprocessorSpec):
        self.spec = spec
        self.speech_repo = SpeechRepository()
        self.speech_text_repo = SpeechTextRepository()
        self.raw_text_repo = RawTextRepository()
        self.clean_text_repo = CleanTextRepository()

    def execute(self) -> CleanText:
        # 1. Get Speech
        speech = self.speech_repo.get_by_id(self.spec.speech)
        if speech is None:
            raise ValueError(f"No Speech found for id: {self.spec.speech}")
        # 2. Get SpeechText
        speech_text = self.speech_text_repo.get_by_id(speech.text)
        if speech_text is None:
            raise ValueError(f"No SpeechText found for id: {speech.text}")
        # 3. Get RawText
        raw_text = self.raw_text_repo.get_by_id(speech_text.raw_text)
        if raw_text is None:
            raise ValueError(f"No RawText found for id: {speech_text.raw_text}")
        # 4. Preprocess
        language_code = speech_text.language_code
        preprocessor_cls = PreprocessRawText.pick_preprocessor(language_code)
        if preprocessor_cls is None:
            raise ValueError(f"No preprocessor found for language: {language_code}")
        service = PreprocessRawText(raw_text, language_code)
        clean_dto = service.process(preprocessor_cls)
        clean_text = CleanText(
            id=UUID.new(),
            speech_text_id=speech_text.id,
            text=clean_dto.text
        )
        self.clean_text_repo.add(clean_text)
        # 5. Update SpeechText with CleanText id
        speech_text.clean_text = clean_text.id
        self.speech_text_repo.update(speech_text)
        return clean_text