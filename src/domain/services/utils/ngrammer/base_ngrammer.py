from abc import ABC, abstractmethod
from src.domain.models.common.a_corpora import Corpora

class Ngrammer(ABC):
    """
    Base class for n-gram generators.
    """
    @abstractmethod
    def generate_ngrams_external(cls, corpora: Corpora, n: int) -> Corpora:
        """
        Generate n-grams using an external library or method.
        Returns the corpora with updated ngram_tokens in each speech text.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def generate_ngrams(self, corpora: Corpora, n: int) -> Corpora:
        """
        Generate n-grams from corpora.
        Returns the corpora with updated ngram_tokens in each speech text.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def find_by_specifications(cls, language_code):
        for subclass in cls.__subclasses__():
            if getattr(subclass, 'language_code', None) == language_code:
                return subclass
        return None
    
