from typing import List, Literal
from split_words import Splitter # type: ignore
from src.domain.services.text.preprocessor.stopwords.german_stopwords import GermanStopwords
import unicodedata

class GermanNormalizer:
    _splitter = Splitter()

    @staticmethod
    def _recursive_split(word: str, min_score: float = 0.5) -> list[str]:
        """
        Recursively split a compound word using the Splitter.
        Returns a list of subwords; if no split meets min_score, returns [word].
        """
        # Attempt to split the compound
        candidates = GermanNormalizer._splitter.split_compound(word)
        if not candidates:
            return [word]
        # Pick best candidate by highest score
        best_score, left, right = max(candidates, key=lambda x: x[0])
        # If score is below threshold, do not split
        if best_score < min_score:
            return [word]
        # Recursively split each side
        parts: List[str] = []
        parts.extend(GermanNormalizer._recursive_split(left, min_score))
        parts.extend(GermanNormalizer._recursive_split(right, min_score))
        return parts

    @classmethod
    def split_compounds(cls, text: str, min_score: float = 0.5) -> str:
        words = text.split()
        normalized_words: list[str] = []
        for word in words:
            try:
                parts = cls._recursive_split(word, min_score)
                if len(parts) == 1:
                    # No split performed
                    normalized_words.append(word)
                else:
                    normalized_words.extend(parts)
            except Exception as e:
                print(f"Error splitting '{word}': {e}") # TODO: add proper logging
                normalized_words.append(word)
        return ' '.join(normalized_words)
    
    @staticmethod
    def normalize_unicode(text: str, form: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFKD", strip_diacritics: bool = False) -> str:
        """
        Normalize unicode characters in the text. Optionally strip diacritics.
        Args:
            text: Input string to normalize.
            form: Unicode normalization form (NFC, NFD, NFKC, NFKD).
            strip_diacritics: If True, remove diacritics from characters.
        Returns:
            Normalized string.
        """
        normalized = unicodedata.normalize(form, text)
        if strip_diacritics:
            normalized = "".join(
                c for c in normalized if not unicodedata.combining(c)
            )
        return normalized
    

    @staticmethod
    def remove_artifacts(text: str) -> str:
        pattern = GermanStopwords().compile_field_artifact_pattern()
        return pattern.sub("", text)

