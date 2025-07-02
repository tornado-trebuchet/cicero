from src.domain.models.text.v_text_raw import RawText
from src.domain.models.text.v_text_clean import CleanText
from src.domain.services.text.base_text_service import TextService
from src.domain.services.utils.preprocessor.base_preprocessor import Preprocessor

class PreprocessRawText(TextService):
    def __init__(self, raw_text: RawText, language_code):
        self.raw_text = raw_text
        self.language_code = language_code
        self.clean_text = CleanText

    @staticmethod
    def pick_preprocessor(language_code):
        return Preprocessor.find_by_specifications(language_code=language_code)

    def process(self) -> CleanText:
        preprocessor_cls = None
        if self.language_code:
            preprocessor_cls = self.pick_preprocessor(self.language_code)
        if preprocessor_cls:
            self.clean_text = preprocessor_cls().process(self.raw_text)
        else:
            raise ValueError("No suitable preprocessor found for the given language code.")
        return self.clean_text
