from abc import ABC, abstractmethod

from src.domain.models.common.v_enums import LanguageEnum


class Stopwords(ABC):

    language_code: LanguageEnum

    @classmethod
    def find_by_specifications(cls, language_code: LanguageEnum):
        for subclass in cls.__subclasses__():
            if getattr(subclass, "language_code", None) == language_code:
                return subclass
        return None

    @property
    @abstractmethod
    def field_artifacts(self) -> set[str]:
        """E.g. parliamentary notation of laughter / objections / announcements"""
        pass

    @property
    @abstractmethod
    def special_stopwords(self) -> set[str]:
        """Empirically derived from processed data"""
        pass

    @property
    @abstractmethod
    def general_stopwords(self) -> set[str]:
        pass

    @property
    @abstractmethod
    def post_processing_stopwords(self) -> set[str]:
        pass

    @abstractmethod
    def get_stopwords(self) -> set[str]:
        """
        Get the stopwords for the specified language.
        """
        pass

    @property
    def all_stopwords(self) -> set[str]:
        stopwords: set[str] = set()
        stopwords.update(self.general_stopwords)
        stopwords.update(self.special_stopwords)
        stopwords.update(self.field_artifacts)
        return stopwords
