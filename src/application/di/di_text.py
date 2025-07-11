from src.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from src.infrastructure.repository.pgsql.text.rep_speech_text import SpeechTextRepository
from src.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository
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


# ============= Repository Injection ==============

def get_protocol_repository():
    return ProtocolRepository()

def get_speech_text_repository():
    return SpeechTextRepository()

def get_speech_repository():
    return SpeechRepository()

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

def get_list_protocols_use_case():
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


