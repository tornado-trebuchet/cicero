from src.domain.models.text.e_text_raw import RawText
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.services.text.preprocessor.serv_preprocessor_dto import (
    CleanTextDTO,
)

from src.domain.services.text.preprocessor.preprocessors.base_preprocessor import Preprocessor
from src.domain.services.text.preprocessor.normalizer.german_normalizer import GermanNormalizer
#import spacy

class GermanPreprocessor(Preprocessor):
    language_code = LanguageEnum.DE
    def __init__(self):
        super().__init__()
        #self.nlp = spacy.load("de_core_news_lg")
        self.normalizer = GermanNormalizer()

    def clean(self, raw_text: RawText) -> CleanTextDTO:
        text = raw_text.text
        text = self.normalizer.normalize_unicode(text, form= "NFKD", strip_diacritics=False)
        text = text.strip()
        text = " ".join(text.split())
        #text = self.normalizer.split_compounds(text)
        #doc = self.nlp(text)
        return CleanTextDTO(text)
