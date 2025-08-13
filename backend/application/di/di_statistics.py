from backend.application.use_cases.statistics.statistics import StatisticsUseCase
from backend.application.di.di_pgsql import (
    get_country_repository,
    get_institution_repository,
    get_party_repository,
    get_period_repository,
    get_speaker_repository,
    get_protocol_repository,
    get_speech_repository,
)

def get_statistics_use_case():
    return StatisticsUseCase(
        country_repo=get_country_repository(),
        institution_repo=get_institution_repository(),
        party_repo=get_party_repository(),
        period_repo=get_period_repository(),
        speaker_repo=get_speaker_repository(),
        protocol_repo=get_protocol_repository(),
        speech_repo=get_speech_repository(),
    )