from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.e_text_clean import CleanText
from src.domain.services.text.tokenizer.serv_tokenizer_dto import TokenizedTextDTO
from src.domain.services.text.base_text_service import TextService
from src.domain.services.text.preprocessor.stopwords.base_stopwords import (
    Stopwords,
)
from src.domain.services.text.tokenizer.tokenizers.base_tokenizer import Tokenizer


class TokenizeCleanText(TextService):
    def __init__(self, clean_text: CleanText, language_code: LanguageEnum):
        super().__init__(config=None)
        self.clean_text = clean_text
        self.language_code = language_code

    @staticmethod
    def pick_tokenizer(language_code: LanguageEnum):
        return Tokenizer.find_by_specifications(language_code=language_code)

    @staticmethod
    def pick_stopwords(language_code: LanguageEnum):
        return Stopwords.find_by_specifications(language_code=language_code)

    def process(self, tokenizer_cls: type[Tokenizer], stopwords_list: set[str]) -> TokenizedTextDTO:
        tokens = tokenizer_cls().tokenize(self.clean_text)
        filtered_tokens = [
            token
            for token in tokens.tokens
            if token.lower() not in stopwords_list
        ]
        return TokenizedTextDTO(tokens=filtered_tokens)
