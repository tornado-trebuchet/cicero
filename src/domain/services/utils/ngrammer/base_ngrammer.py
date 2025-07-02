from abc import ABC, abstractmethod
from src.domain.models.text.v_text_tokenized import Tokens
from src.domain.models.text.v_text_ngrams import NGramTokens

# FIXME generates ngrams from sentences, not tokens
class Ngrammer(ABC):
    """
    Base class for n-gram generators.
    """
    @abstractmethod
    def generate_ngrams_external(cls, corpora: list[list[Tokens]], n: int) -> list[list[Tokens]]:
        """
        Generate n-grams using an external library or method.
        This method can be overridden by subclasses if needed.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def generate_ngrams(self, tokens: Tokens, n: int) -> NGramTokens:
        """
        Generate n-grams from a Tokens object.
        Should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def find_by_specifications(cls, language_code):
        for subclass in cls.__subclasses__():
            if getattr(subclass, 'language_code', None) == language_code:
                return subclass
        return None
    
