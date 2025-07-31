from .common.i_corpora import ICorporaRepository
from .context.i_country import ICountryRepository
from .context.i_institution import IInstitutionRepository
from .context.i_party import IPartyRepository
from .context.i_period import IPeriodRepository
from .context.i_speaker import ISpeakerRepository
from .text.i_protocol import IProtocolRepository
from .text.i_speech import ISpeechRepository
from .text.i_speech_text import ISpeechTextRepository
from .text.i_text_clean import ICleanTextRepository
from .text.i_text_ngrams import INGramizedTextRepository
from .text.i_text_raw import IRawTextRepository
from .text.i_text_split import ITextSentencesRepository
from .text.i_text_tokenized import ITokenizedTextRepository
from .text.i_text_translated import ITranslatedTextRepository

__all__ = [
    "ICorporaRepository",
    "ICountryRepository",
    "IInstitutionRepository",
    "IPartyRepository",
    "IPeriodRepository",
    "ISpeakerRepository",
    "IProtocolRepository",
    "ISpeechRepository",
    "ICleanTextRepository",
    "INGramizedTextRepository",
    "IRawTextRepository",
    "ITextSentencesRepository",
    "ITokenizedTextRepository",
    "ITranslatedTextRepository",
    "ISpeechTextRepository",
]
