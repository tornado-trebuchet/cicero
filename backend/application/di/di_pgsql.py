from backend.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from backend.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from backend.infrastructure.repository.pgsql.context.rep_party import PartyRepository
from backend.infrastructure.repository.pgsql.context.rep_period import PeriodRepository
from backend.infrastructure.repository.pgsql.context.rep_speaker import SpeakerRepository
from backend.infrastructure.repository.pgsql.text.rep_protocol import ProtocolRepository
from backend.infrastructure.repository.pgsql.text.rep_speech import SpeechRepository

# Repository injection functions

def get_country_repository():
    return CountryRepository()

def get_institution_repository():
    return InstitutionRepository()

def get_party_repository():
    return PartyRepository()

def get_period_repository():
    return PeriodRepository()

def get_speaker_repository():
    return SpeakerRepository()

def get_protocol_repository():
    return ProtocolRepository()

def get_speech_repository():
    return SpeechRepository()