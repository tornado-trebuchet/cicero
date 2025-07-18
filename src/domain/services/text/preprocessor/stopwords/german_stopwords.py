from src.domain.models.common.v_enums import LanguageEnum
from src.domain.services.utils.stopwords.base_stopwords import Stopwords


class GermanStopwords(Stopwords):
    @property
    def language_code(self) -> LanguageEnum:
        return LanguageEnum.DE

    @property
    def field_artifacts(self) -> set[str]:
        return {"lachen", "beifall", "widerspruch"}

    @property
    def special_stopwords(self) -> set[str]:
        return {"äh", "hm", "tja", "naja"}

    @property
    def general_stopwords(self) -> set[str]:
        return {
            "und",
            "oder",
            "aber",
            "nicht",
            "kein",
            "eine",
            "der",
            "die",
            "das",
            "ist",
            "in",
            "zu",
            "den",
            "von",
            "mit",
            "auf",
            "für",
            "an",
            "im",
            "es",
            "dem",
            "als",
            "auch",
            "am",
            "aus",
            "bei",
            "sich",
            "nach",
            "wie",
            "so",
            "wir",
            "er",
            "sie",
            "ich",
            "man",
            "noch",
            "nur",
            "schon",
            "wenn",
            "über",
            "dass",
            "wir",
            "was",
            "wird",
            "sind",
        }

    @property
    def post_processing_stopwords(self) -> set[str]:
        return set()

    def get_stopwords(self) -> set[str]:
        return self.all_stopwords
