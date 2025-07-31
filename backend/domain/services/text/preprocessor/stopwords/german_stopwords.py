from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.preprocessor.stopwords.base_stopwords import Stopwords
import regex  # type: ignore


class GermanStopwords(Stopwords):

    language_code = LanguageEnum.DE

    @property
    def field_artifacts(self) -> set[str]:
        return {"Lachen", "Beifall", "Widerspruch", "Heiterkeit", "Zuruf"}

    def compile_field_artifact_pattern(self):
        # Build a recursive regex to match balanced parentheses with artifact names
        names = "|".join(self.field_artifacts)
        pattern = rf"\(({names})(?:(?:[^()]+)|(?R))*\)"
        return regex.compile(pattern)

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
