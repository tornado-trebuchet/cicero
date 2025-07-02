from src.domain.models.common.v_enums import LanguageEnum
from src.domain.services.text.base_text_service import TextService
from src.domain.services.utils.ngrammer.base_ngrammer import Ngrammer
from src.domain.models.common.a_corpora import Corpora

class NGramTokenizeCleanText(TextService):
    def __init__(self, corpora: Corpora, language_code: LanguageEnum):
        super().__init__(config=None)
        self.corpora = corpora
        self.language_code = language_code
        self.ngrammer = self.pick_ngrammer(self.language_code)()

    def pick_ngrammer(self, language_code: LanguageEnum) -> type:
        ngrammer_cls = Ngrammer.find_by_specifications(language_code)
        if ngrammer_cls is not None:
            return ngrammer_cls
        else:
            raise ValueError(f"No ngrammer found for language code: {language_code}")

    def process(self, n: int) -> Corpora:
        corpora = self.ngrammer.generate_ngrams_external(self.corpora, n)
        return corpora