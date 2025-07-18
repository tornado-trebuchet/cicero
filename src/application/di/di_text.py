from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
from src.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_ngrams import NGramizedTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_split import TextSentencesRepository
from src.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
from src.infrastructure.repository.pgsql.text.rep_text_translated import TranslatedTextRepository
from src.application.use_cases.text.get_by import (
    GetProtocolByIdUseCase,
    GetProtocolsByCountryIdUseCase,
    GetProtocolsByInstitutionIdUseCase,
    GetProtocolsByInstitutionAndPeriodUseCase,
    GetProtocolsByDateRangeUseCase,
    GetSpeechTextByIdUseCase,
    GetSpeechByIdUseCase,
    GetSpeechesByProtocolIdUseCase,
    GetSpeechesBySpeakerIdUseCase,
    GetSpeechesByDateRangeUseCase,
)
from src.application.use_cases.text.list import ListProtocolsUseCase
from src.application.use_cases.text.delete import (
    DeleteProtocolUseCase,
    DeleteSpeechUseCase,
    DeleteTextCleanUseCase,
    DeleteNGramizedTextUseCase,
    DeleteTextRawUseCase,
    DeleteTextSplitUseCase,
    DeleteTokenizedTextUseCase,
    DeleteTranslatedTextUseCase,
    DeleteSpeechTextUseCase,
)

# TODO: properly rename these morons everywhere 
# ============= Repository Injection ==============

def get_protocol_repository():
    return ProtocolRepository()

def get_speech_text_repository():
    return SpeechTextRepository()

def get_speech_repository():
    return SpeechRepository()

def get_clean_text_repository():
    return CleanTextRepository()

def get_ngramized_text_repository():
    return NGramizedTextRepository()

def get_raw_text_repository():
    return RawTextRepository()

def get_text_split_repository():
    return TextSentencesRepository()

def get_tokenized_text_repository():
    return TokenizedTextRepository()

def get_translated_text_repository():
    return TranslatedTextRepository()

# ============= UseCase Injection ==============

def get_protocol_by_id_use_case():
    return GetProtocolByIdUseCase(get_protocol_repository())

def get_protocols_by_country_id_use_case():
    return GetProtocolsByCountryIdUseCase(get_protocol_repository())

def get_protocols_by_institution_id_use_case():
    return GetProtocolsByInstitutionIdUseCase(get_protocol_repository())

def get_protocols_by_institution_and_period_use_case():
    return GetProtocolsByInstitutionAndPeriodUseCase(get_protocol_repository())

def get_protocols_by_date_range_use_case():
    return GetProtocolsByDateRangeUseCase(get_protocol_repository())

def list_protocols_use_case():
    return ListProtocolsUseCase(get_protocol_repository())

def get_speech_text_by_id_use_case():
    return GetSpeechTextByIdUseCase(get_speech_text_repository())

def get_speech_by_id_use_case():
    return GetSpeechByIdUseCase(get_speech_repository())

def get_speeches_by_protocol_id_use_case():
    return GetSpeechesByProtocolIdUseCase(get_speech_repository())

def get_speeches_by_speaker_id_use_case():
    return GetSpeechesBySpeakerIdUseCase(get_speech_repository())

def get_speeches_by_date_range_use_case():
    return GetSpeechesByDateRangeUseCase(get_speech_repository())

def delete_protocol_use_case():
    return DeleteProtocolUseCase(get_protocol_repository())

def delete_speech_use_case():
    return DeleteSpeechUseCase(get_speech_repository())

def delete_text_clean_use_case():
    return DeleteTextCleanUseCase(get_clean_text_repository())

def delete_ngramized_text_use_case():
    return DeleteNGramizedTextUseCase(get_ngramized_text_repository())

def delete_text_raw_use_case():
    return DeleteTextRawUseCase(get_raw_text_repository())

def delete_text_split_use_case():
    return DeleteTextSplitUseCase(get_text_split_repository())

def delete_tokenized_text_use_case():
    return DeleteTokenizedTextUseCase(get_tokenized_text_repository())

def delete_translated_text_use_case():
    return DeleteTranslatedTextUseCase(get_translated_text_repository())

def delete_speech_text_use_case():
    return DeleteSpeechTextUseCase(get_speech_text_repository())


