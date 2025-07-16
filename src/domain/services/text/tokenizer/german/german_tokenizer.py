from src.domain.services.utils.tokenizer.base_tokenizer import Tokenizer
from src.domain.models.common.v_enums import LanguageEnum
from domain.models.text.e_text_clean import CleanText
from domain.models.text.e_text_tokenized import TokenizedText
import spacy
# importing spacy model

class GermanTokenizer(Tokenizer):
    """Tokenizer for German language."""

    @property
    def language_code(self) -> LanguageEnum:
        return LanguageEnum.DE

    def tokenize_external_lib(self, clean_text: CleanText) -> TokenizedText:
        #lazy loading that shitter
        nlp = spacy.load('de_core_news_sm')
        doc = nlp(clean_text.text)
        tokens = [token.text for token in doc]
        return TokenizedText(tokens=tokens)

    def tokenize(self, clean_text: CleanText) -> TokenizedText:
        text = clean_text.text
        tokens = text.split()
        return TokenizedText(tokens=tokens)

    def stem(self, tokens: list[str]) -> list[str]:
        # TODO
        return tokens

    def lemmatize(self, tokens: list[str]) -> list[str]:
        # TODO
        return tokens
