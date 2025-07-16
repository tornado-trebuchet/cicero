from abc import ABC, abstractmethod
from src.domain.models.common.v_enums import LanguageEnum
from domain.models.text.e_text_clean import CleanText
from domain.models.text.e_text_tokenized import TokenizedText

class Tokenizer(ABC):
    """
    Base class for tokenizers.
    """

    @property
    @abstractmethod
    def language_code(self) -> LanguageEnum:
        """Return the language code for the tokenizer."""
        pass

    @abstractmethod
    def tokenize_external_lib(self, clean_text: CleanText) -> TokenizedText:
        """
        Perform any necessary preprocessing or magic using spaCy.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def tokenize(self, clean_text: CleanText) -> TokenizedText:
        """
        Tokenize the input text and return a list of tokens.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def stem(self, tokens: list[str]) -> list[str]:
        """
        Stem the tokens and return a list of stemmed tokens.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def lemmatize(self, tokens: list[str]) -> list[str]:
        """
        Lemmatize the tokens and return a list of lemmatized tokens.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def find_by_specifications(cls, language_code: LanguageEnum):
        """
        Find a tokenizer class matching the given language_code.
        Returns the class if found, else None.
        """
        for subclass in cls.__subclasses__():
            if getattr(subclass, 'language_code', None) == language_code:
                return subclass
        return None