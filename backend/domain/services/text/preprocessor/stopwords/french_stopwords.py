from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.preprocessor.stopwords.base_stopwords import Stopwords


class FrenchStopwords(Stopwords):

    language_code = LanguageEnum.FR

    @property
    def field_artifacts(self) -> set[str]:
        return {"rire", "applaudissements", "objection"}

    @property
    def special_stopwords(self) -> set[str]:
        return {"euh", "hein", "bah", "ben"}

    @property
    def general_stopwords(self) -> set[str]:
        return {
            "le",
            "la",
            "les",
            "un",
            "une",
            "et",
            "ou",
            "mais",
            "dans",
            "en",
            "du",
            "des",
            "ce",
            "cette",
            "il",
            "elle",
            "on",
            "nous",
            "vous",
            "ils",
            "elles",
            "ne",
            "pas",
            "que",
            "qui",
            "pour",
            "par",
            "avec",
            "sur",
            "se",
            "au",
            "aux",
            "son",
            "sa",
            "ses",
            "leur",
            "leurs",
            "y",
            "a",
            "de",
            "d'",
            "l'",
        }

    @property
    def post_processing_stopwords(self) -> set[str]:
        return set()

    def get_stopwords(self) -> set[str]:
        return self.all_stopwords
