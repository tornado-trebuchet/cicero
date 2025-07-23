from gensim.models.phrases import Phraser, Phrases

from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_enums import LanguageEnum
from src.domain.models.text.e_text_ngrams import NGramizedText
from src.domain.services.text.ngrammer.base_ngrammer import Ngrammer


# Processes corpora by extracting sentences and applying gensim n-gram generation
class GermanNgrammer(Ngrammer):
    language_code = LanguageEnum.DE

    def generate_ngrams(self, corpora: Corpora, n: int) -> Corpora:
        """Generate n-grams using simple sliding window approach."""
        for speech in corpora.speeches:
            if speech.text.sentences is None:
                speech.text.split_sentences()

            # Type guard: sentences should now be available
            if speech.text.sentences is not None and speech.text.sentences.sentences is not None:
                sentences = speech.text.sentences.sentences
                ngrams = []
                for sentence in sentences:
                    words = sentence.split()
                    sentence_ngrams = (
                        [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)] if n > 0 else []
                    )
                    ngrams.extend(sentence_ngrams)

                speech.text.ngram_tokens = NGramizedText(tokens=ngrams)

        return corpora

    def generate_ngrams_external(self, corpora: Corpora, n: int) -> Corpora:
        """Generate n-grams using gensim for better phrase detection across the entire corpus."""
        # Extract all sentences from all speeches for corpus-wide phrase detection
        all_sentences = []
        speech_sentence_counts = []

        for speech in corpora.speeches:
            if speech.text.sentences is None:
                speech.text.split_sentences()
            # FIXME: need to test with actual gensim
            if speech.text.sentences is not None and speech.text.sentences.sentences is not None:
                sentences = speech.text.sentences.sentences
                # Split sentences into word lists for gensim
                sentence_word_lists = [sentence.split() for sentence in sentences]
                all_sentences.extend(sentence_word_lists)
                speech_sentence_counts.append(len(sentence_word_lists))

        # Apply gensim phrase detection
        if n == 2:
            phrases = Phrases(all_sentences, min_count=1, threshold=1)
            phraser = Phraser(phrases)
            ngrammed_sentences = [list(phraser[sent]) for sent in all_sentences]
        elif n == 3:
            # First pass: bigrams
            phrases = Phrases(all_sentences, min_count=1, threshold=1)
            bigram_phraser = Phraser(phrases)
            bigrammed = [list(bigram_phraser[sent]) for sent in all_sentences]
            # Second pass: trigrams
            trigram_phrases = Phrases(bigrammed, min_count=1, threshold=1)
            trigram_phraser = Phraser(trigram_phrases)
            ngrammed_sentences = [list(trigram_phraser[sent]) for sent in bigrammed]
        else:
            raise ValueError(f"N-gram size {n} is not supported. Only 2-grams and 3-grams are supported.")

        # Reconstruct the corpora structure in-place
        sentence_idx = 0
        for speech_idx, speech in enumerate(corpora.speeches):
            speech_sentence_count = speech_sentence_counts[speech_idx]
            speech_ngrams = []

            # Collect all n-grams for this speech
            for i in range(speech_sentence_count):
                speech_ngrams.extend(ngrammed_sentences[sentence_idx + i])

            speech.text.ngram_tokens = NGramizedText(tokens=speech_ngrams)
            sentence_idx += speech_sentence_count

        return corpora
