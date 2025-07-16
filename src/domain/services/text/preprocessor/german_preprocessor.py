from .base_preprocessor import Preprocessor
from domain.models.text.e_text_raw import RawText
from domain.models.text.e_text_clean import CleanText
from src.domain.models.common.v_enums import LanguageEnum

class GermanPreprocessor(Preprocessor):
    
    language_code = LanguageEnum.DE

    def process(self, raw_text: RawText) -> CleanText:
        text = raw_text.text
        text = text.strip()
        text = ' '.join(text.split())  
        text = text.lower()
        clean_text = CleanText(text=text)
        return clean_text
