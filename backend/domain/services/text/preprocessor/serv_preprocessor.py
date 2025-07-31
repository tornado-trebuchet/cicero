from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.models.text.e_text_raw import RawText
from backend.domain.services.text.base_text_service import TextService
from backend.domain.services.text.preprocessor.preprocessors.base_preprocessor import Preprocessor
from backend.domain.services.text.preprocessor.serv_preprocessor_dto import CleanTextDTO
import logging

logger = logging.getLogger(__name__)


class PreprocessRawText(TextService):
    def __init__(self, raw_text: RawText, language_code: LanguageEnum):
        self.raw_text = raw_text
        self.language_code = language_code
        self.clean_text: CleanTextDTO | None = None

    @staticmethod
    def pick_preprocessor(language_code: LanguageEnum):
        logger.debug(f"Picking preprocessor for language_code={language_code}")
        return Preprocessor.find_by_specifications(language_code=language_code)

    def process(self, preprocessor_cls: type[Preprocessor]) -> CleanTextDTO:
        logger.debug(f"Processing raw text with preprocessor_cls={preprocessor_cls}")
        self.clean_text = preprocessor_cls().clean(self.raw_text)
        logger.debug(f"Cleaned text: {self.clean_text}")
        return self.clean_text
