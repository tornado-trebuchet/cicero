from domain.services.utils.ngrammer.base_ngrammer import Ngrammer
from src.domain.models.text.v_tokenized_text import Tokens
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.v_ngram_tokens import NGramTokens
from gensim.models.phrases import Phrases, Phraser
# importing gensim

class GermanNgrammer(Ngrammer):
    language_code = LanguageEnum.DE

    def generate_ngrams(self, tokens: Tokens, n: int) -> NGramTokens:
        token_list = tokens.tokens
        ngrams = [' '.join(token_list[i:i+n]) for i in range(len(token_list)-n+1)] if n > 0 else []
        return NGramTokens(tokens=ngrams)

    def generate_ngrams_external(self, corpora: list[list[Tokens]], n: int) -> list[list[Tokens]]:
        # Flatten all sentences from all texts, extracting the token lists from each Tokens object
        all_sentences = [sentence.tokens for text in corpora for sentence in text]
        if n == 2:
            phrases = Phrases(all_sentences, min_count=1, threshold=1)
            bigram = Phraser(phrases)
            ngrammed_sentences = [list(bigram[sent]) for sent in all_sentences]
        elif n == 3:
            phrases = Phrases(all_sentences, min_count=1, threshold=1)
            bigram = Phraser(phrases)
            bigrammed = [list(bigram[sent]) for sent in all_sentences]
            trigram_phrases = Phrases(bigrammed, min_count=1, threshold=1)
            trigram = Phraser(trigram_phrases)
            ngrammed_sentences = [list(trigram[sent]) for sent in bigrammed]
        else:
            raise ValueError(f"N-gram size {n} is not supported. Only 2-grams and 3-grams are supported.")
        # Reconstruct corpora structure, wrapping ngrammed tokens back into Tokens objects
        ngrammed_corpora = []
        idx = 0
        for text in corpora:
            n_sents = len(text)
            ngrammed_text = [Tokens(tokens=ngrammed_sentences[idx + i]) for i in range(n_sents)]
            ngrammed_corpora.append(ngrammed_text)
            idx += n_sents
        return ngrammed_corpora

