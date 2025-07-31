from abc import ABC, abstractmethod

from backend.domain.models.text.e_text_raw import RawText
from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.preprocessor.serv_preprocessor_dto import (
    CleanTextDTO,
)


class Preprocessor(ABC):

    language_code: LanguageEnum

    @classmethod
    def find_by_specifications(cls, language_code: LanguageEnum):
        for subclass in cls.__subclasses__():
            if getattr(subclass, "language_code") == language_code:
                return subclass
        return None

    @abstractmethod
    def clean(self, raw_text: RawText) -> CleanTextDTO:
        raise NotImplementedError("Subclasses must implement this method.")
