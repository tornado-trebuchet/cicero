from src.domain.services.utils.stopwords.base_stopwords import Stopwords
from src.domain.models.common.v_enums import LanguageEnum

class EnglishStopwords(Stopwords):
    @property
    def language_code(self) -> LanguageEnum:
        return LanguageEnum.EN

    @property
    def field_artifacts(self) -> set[str]:
        return {"laughter", "applause", "objection"}

    @property
    def special_stopwords(self) -> set[str]:
        return {"uh", "um", "er", "ah"}

    @property
    def general_stopwords(self) -> set[str]:
        return {
            "the", "and", "is", "in", "it", "you", "that", "he", "was", "for", "on", "are", "with", "as", "I", "his", "they", "be", "at", "one", "have", "this", "from", "or", "had", "by", "not", "word", "but", "what", "some", "we", "can", "out", "other", "were", "all", "there", "when", "up", "use", "your", "how", "said", "an", "each", "she"
        }

    @property
    def post_processing_stopwords(self) -> set[str]:
        return set()

    def get_stopwords(self) -> set[str]:
        return self.all_stopwords
