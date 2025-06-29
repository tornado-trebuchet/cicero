import re
from abc import ABC, abstractmethod

class RegexPattern(ABC):
    """
    Abstract base class for all regex pattern classes.
    Enforces required metadata and a compile method contract.
    """
    country_code = None
    institution_code = None
    language_code = None
    protocol_type = None

    @classmethod
    @abstractmethod
    def compile_pattern(cls) -> re.Pattern[str]:
        """
        Should return a compiled regex pattern (re.Pattern).
        """
        pass

    @classmethod
    def find_by_specifications(cls, country_code=None, institution_code=None, language_code=None, protocol_type=None):
        """
        Find a subclass matching the given specifications.
        Returns the class if found, else None.
        """
        for subclass in cls.__subclasses__():
            if ((country_code is None or getattr(subclass, 'country_code', None) == country_code) and
                (institution_code is None or getattr(subclass, 'institution_code', None) == institution_code) and
                (language_code is None or getattr(subclass, 'language_code', None) == language_code) and
                (protocol_type is None or getattr(subclass, 'protocol_type', None) == protocol_type)):
                return subclass
        return None
