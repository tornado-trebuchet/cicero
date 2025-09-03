from dataclasses import dataclass

from backend.domain.irepository.context.i_country import ICountryRepository
from backend.domain.irepository.context.i_institution import IInstitutionRepository
from backend.domain.irepository.context.i_party import IPartyRepository
from backend.domain.irepository.context.i_period import IPeriodRepository
from backend.domain.irepository.context.i_speaker import ISpeakerRepository
from backend.domain.irepository.text.i_protocol import IProtocolRepository
from backend.domain.irepository.text.i_speech import ISpeechRepository

@dataclass
class AppStatistics:
    total_countries: int
    total_institutions: int
    total_speeches: int
    total_speakers: int
    total_protocols: int

class StatisticsUseCase:
    def __init__(
        self,
        country_repo: ICountryRepository,
        institution_repo: IInstitutionRepository,
        party_repo: IPartyRepository,
        period_repo: IPeriodRepository,
        speaker_repo: ISpeakerRepository,
        protocol_repo: IProtocolRepository,
        speech_repo: ISpeechRepository,
    ):
        self.country_repo = country_repo
        self.institution_repo = institution_repo
        self.party_repo = party_repo
        self.period_repo = period_repo
        self.speaker_repo = speaker_repo
        self.protocol_repo = protocol_repo
        self.speech_repo = speech_repo
#FIXME: relete and rework with proper query
        total_countries = len(self.country_repo.list())
        total_institutions = len(self.institution_repo.list())
        total_speeches = len(self.speech_repo.list())
        total_speakers = len(self.speaker_repo.list())
        total_protocols = len(self.protocol_repo.list())
        return AppStatistics(
            total_countries=total_countries,
            total_institutions=total_institutions,
            total_speeches=total_speeches,
            total_speakers=total_speakers,
            total_protocols=total_protocols,
        )
