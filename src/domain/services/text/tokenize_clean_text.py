from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.v_clean_text import CleanText
from src.domain.models.text.v_tokenized_text import Tokens
from src.domain.services.text.base_text_service import TextService
from src.domain.services.utils.tokenizer.base_tokenizer import Tokenizer
from src.domain.services.utils.stopwords.base_stopwords import Stopwords


class TokenizeCleanText(TextService):
    def __init__(self, clean_text: CleanText, language_code: LanguageEnum):
        super().__init__(config=None)
        self.clean_text = clean_text
        self.language_code = language_code 
        self.tokenizer = self.pick_tokenizer(self.language_code)()
        self.stopwords = self.pick_stopwords(self.language_code).get_stopwords()

    def pick_tokenizer(self, language_code: LanguageEnum) -> type:
        """From utils"""
        tokenizer_cls = Tokenizer.find_by_specifications(language_code)
        if tokenizer_cls is not None:
            return tokenizer_cls
        else:
            raise ValueError(f"No tokenizer found for language code: {language_code}")
        
    def pick_stopwords(self, language_code: LanguageEnum):
        """From utils"""
        stopwords_cls = Stopwords.find_by_specifications(language_code)
        if stopwords_cls is not None:
            return stopwords_cls(language_code)
        else:
            raise ValueError(f"No stopwords found for language code: {language_code}")

    def process(self, clean_text: CleanText) -> Tokens:
        tokens = self.tokenizer.tokenize_external_lib(clean_text)
        filtered_tokens = [token for token in tokens.tokens if token.lower() not in self.stopwords]
        return Tokens(tokens=filtered_tokens)