from src.domain.models.text.e_text_raw import RawText
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.services.text.preprocessor.serv_preprocessor_dto import (
    CleanTextDTO,
)

from .base_preprocessor import Preprocessor


class GermanPreprocessor(Preprocessor):

    language_code = LanguageEnum.DE

    def clean(self, raw_text: RawText) -> CleanTextDTO:
        text = raw_text.text
        text = text.strip()
        text = " ".join(text.split())
        text = text.lower()
        clean_text = CleanTextDTO(text=text)
        return clean_text
