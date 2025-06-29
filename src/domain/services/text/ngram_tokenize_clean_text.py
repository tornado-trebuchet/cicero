from src.domain.models.text.v_clean_text import CleanText
from src.domain.models.common.v_enums import LanguageEnum
from domain.models.text.v_tokenized_text import Tokens
from src.domain.services.text.base_text_service import TextService

class NGramTokenizeCleanText(TextService):
    """
    Service to tokenize clean text and update the CleanText object with tokens.
    """
    def __init__(self, clean_text: CleanText):
        self.clean_text = clean_text

    def pick_tokenizer(self, language_code: LanguageEnum) -> NGramTokenizer:
        return NGramTokenizer

    def pick_stopwords(self, language_code: LanguageEnum) -> Stopwords:
        return Stopwords

    def process(self, tokenizer: Tokenizer) -> CleanText:

        self.clean_text.tokens = Tokens(tokens=tokens)
        
        return self.clean_text