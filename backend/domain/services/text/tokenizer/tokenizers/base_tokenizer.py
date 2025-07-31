from abc import ABC, abstractmethod

from backend.domain.models.text.e_text_clean import CleanText
from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.tokenizer.serv_tokenizer_dto import TokenizedTextDTO


class Tokenizer(ABC):
    """
    Base class for tokenizers.
    """

    language_code: LanguageEnum

    @classmethod
    def find_by_specifications(cls, language_code: LanguageEnum):
        for subclass in cls.__subclasses__():
            if getattr(subclass, "language_code", None) == language_code:
                return subclass
        return None

    @abstractmethod
    def tokenize(self, clean_text: CleanText) -> TokenizedTextDTO:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def tokenize_fast(self, clean_text: CleanText) -> TokenizedTextDTO:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def stem(self, tokens: list[str]) -> list[str]:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def lemmatize(self, tokens: list[str]) -> list[str]:
        raise NotImplementedError("Subclasses must implement this method.")
