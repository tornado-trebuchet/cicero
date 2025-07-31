import spacy

from backend.domain.models.text.e_text_clean import CleanText
from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.tokenizer.tokenizers.base_tokenizer import Tokenizer
from backend.domain.services.text.tokenizer.serv_tokenizer_dto import TokenizedTextDTO


class GermanTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("de_core_news_lg")

    language_code = LanguageEnum.DE

    def tokenize(self, clean_text: CleanText) -> TokenizedTextDTO:
        doc = self.nlp(clean_text.text)
        tokens = [token.text for token in doc if not token.is_stop]
        return TokenizedTextDTO(tokens)

    def tokenize_fast(self, clean_text: CleanText) -> TokenizedTextDTO:
        text = clean_text.text
        tokens = text.split()
        return TokenizedTextDTO(tokens)

    def stem(self, tokens: list[str]) -> list[str]:
        # TODO
        return tokens

    def lemmatize(self, tokens: list[str]) -> list[str]:
        # TODO
        return tokens
