from src.domain.services.utils.tokenizer.base_tokenizer import Tokenizer
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.v_clean_text import CleanText
from src.domain.models.text.v_tokenized_text import Tokens
import spacy
# importing spacy

class GermanTokenizer(Tokenizer):
    """
    Tokenizer for German language.
    This class implements the Tokenizer interface for German text.
    """

    @property
    def language_code(self) -> LanguageEnum:
        return LanguageEnum.DE

    def tokenize_external_lib(self, clean_text: CleanText) -> Tokens:
        #lazy loading that shitter
        nlp = spacy.load('de_core_news_sm')
        doc = nlp(clean_text.text)
        tokens = [token.text for token in doc]
        return Tokens(tokens=tokens)

    def tokenize(self, clean_text: CleanText) -> Tokens:
        text = clean_text.text
        tokens = text.split()
        return Tokens(tokens=tokens)

    def stem(self, tokens: list[str]) -> list[str]:
        # Placeholder: return tokens unchanged
        return tokens

    def lemmatize(self, tokens: list[str]) -> list[str]:
        # Placeholder: return tokens unchanged
        return tokens
