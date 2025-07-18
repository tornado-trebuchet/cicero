from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.e_text_raw import RawText
from src.domain.services.text.base_text_service import TextService
from src.domain.services.text.preprocessor.preprocessors.base_preprocessor import (
    Preprocessor,
)
from src.domain.services.text.preprocessor.serv_preprocessor_dto import (
    CleanTextDTO,
)


#
class PreprocessRawText(TextService):
    def __init__(self, raw_text: RawText, language_code: LanguageEnum):
        self.raw_text = raw_text
        self.language_code = language_code

    @staticmethod
    def pick_preprocessor(language_code: LanguageEnum):
        return Preprocessor.find_by_specifications(language_code=language_code)

    def process(self, preprocessor_cls: type[Preprocessor]) -> CleanTextDTO:
        self.clean_text = preprocessor_cls().clean(self.raw_text)
        return self.clean_text
