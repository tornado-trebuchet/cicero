from typing import List, Optional

from src.domain.irepository.text.i_protocol import IProtocolRepository
from src.domain.irepository.text.i_speech import ISpeechRepository
from src.domain.irepository.text.I_speech_text import ISpeechTextRepository
from src.domain.models.common.v_common import UUID, DateTime
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText


class GetProtocolByIdUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, id: UUID):
        return self.repo.get_by_id(id)


class GetProtocolsByCountryIdUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, country_id: UUID):
        return self.repo.get_by_country_id(country_id)


class GetProtocolsByInstitutionIdUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, institution_id: UUID):
        return self.repo.get_by_institution_id(institution_id)


class GetProtocolsByInstitutionAndPeriodUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, institution_id: UUID, period_id: UUID):
        return self.repo.get_by_institution_and_period(
            institution_id, period_id
        )


class GetProtocolsByDateRangeUseCase:
    def __init__(self, repo: IProtocolRepository):
        self.repo = repo

    def execute(self, start_date: DateTime, end_date: DateTime):
        return self.repo.get_by_date_range(start_date, end_date)


class GetSpeechTextByIdUseCase:
    def __init__(self, repo: ISpeechTextRepository):
        self.repo = repo

    def execute(self, id: UUID) -> Optional[SpeechText]:
        return self.repo.get_by_id(id)


class GetSpeechByIdUseCase:
    def __init__(self, repo: ISpeechRepository):
        self.repo = repo

    def execute(self, id: UUID) -> Optional[Speech]:
        return self.repo.get_by_id(id)


class GetSpeechesByProtocolIdUseCase:
    def __init__(self, repo: ISpeechRepository):
        self.repo = repo

    def execute(self, protocol_id: UUID) -> List[Speech]:
        return self.repo.get_by_protocol_id(protocol_id)


class GetSpeechesBySpeakerIdUseCase:
    def __init__(self, repo: ISpeechRepository):
        self.repo = repo

    def execute(self, speaker_id: UUID) -> List[Speech]:
        return self.repo.get_by_speaker_id(speaker_id)


class GetSpeechesByDateRangeUseCase:
    def __init__(self, repo: ISpeechRepository):
        self.repo = repo

    def execute(
        self, start_date: DateTime, end_date: DateTime
    ) -> List[Speech]:
        return self.repo.get_by_date_range(start_date, end_date)
