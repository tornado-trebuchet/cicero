from abc import ABC, abstractmethod
from src.domain.models.text.v_raw_text import RawText
from src.domain.models.text.v_clean_text import CleanText
from src.domain.models.common.v_enums import LanguageEnum

class Preprocessor(ABC):
    """
    Base class for preprocessors.
    """

    def __init__(self):
        pass

    @classmethod
    def find_by_specifications(cls, language_code: LanguageEnum):
        """
        Find a preprocessor class matching the given specifications.
        Returns the class if found, else None.
        """
        for subclass in cls.__subclasses__():
            if getattr(subclass, 'language_code', None) == language_code:
                return subclass
        return None
    
    @abstractmethod
    def process(self, raw_text:RawText) -> CleanText:
        """
        Process the raw text and return a cleaned text object.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
