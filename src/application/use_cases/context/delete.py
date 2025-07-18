from src.domain.irepository.context.i_country import ICountryRepository
from src.domain.irepository.context.i_institution import IInstitutionRepository
from src.domain.irepository.context.i_party import IPartyRepository
from src.domain.irepository.context.i_period import IPeriodRepository
from src.domain.irepository.context.i_speaker import ISpeakerRepository
from src.domain.models.common.v_common import UUID


class DeleteCountryUseCase:
    def __init__(self, repo: ICountryRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteInstitutionUseCase:
    def __init__(self, repo: IInstitutionRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeletePartyUseCase:
    def __init__(self, repo: IPartyRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeletePeriodUseCase:
    def __init__(self, repo: IPeriodRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class DeleteSpeakerUseCase:
    def __init__(self, repo: ISpeakerRepository):
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)
