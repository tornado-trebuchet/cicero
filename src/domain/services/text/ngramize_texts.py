from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.v_tokenized_text import Tokens
from src.domain.models.text.v_ngram_tokens import NGramTokens
from src.domain.services.text.base_text_service import TextService
from src.domain.services.utils.ngrammer.base_ngrammer import Ngrammer
from domain.models.text.v_speech_sentences import Sentences

class NGramTokenizeCleanText(TextService):
    """
    Service to generate n-grams from tokens using a language-specific ngrammer.
    """
    def __init__(self, texts: list[list[Sentences]], language_code: LanguageEnum):
        super().__init__(config=None)
        self.tokens = tokens
        self.language_code = language_code
        self.ngrammer = self.pick_ngrammer(self.language_code)()

    def pick_ngrammer(self, language_code: LanguageEnum) -> type:
        ngrammer_cls = Ngrammer.find_by_specifications(language_code)
        if ngrammer_cls is not None:
            return ngrammer_cls
        else:
            raise ValueError(f"No ngrammer found for language code: {language_code}")

    def process(self, n: int) -> NGramTokens:
        ngram_tokens = self.ngrammer.generate_ngrams_external(self.tokens, n)
        return ngram_tokens