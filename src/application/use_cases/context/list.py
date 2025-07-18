from typing import List

from src.domain.irepository.context.i_country import ICountryRepository
from src.domain.irepository.context.i_institution import IInstitutionRepository
from src.domain.irepository.context.i_party import IPartyRepository
from src.domain.irepository.context.i_period import IPeriodRepository
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_party import Party
from src.domain.models.context.e_period import Period


class ListCountriesUseCase:
    def __init__(self, country_repository: ICountryRepository):
        self.country_repository = country_repository

    def execute(self) -> List[Country]:
        return self.country_repository.list()


class ListInstitutionsUseCase:
    def __init__(self, institution_repository: IInstitutionRepository):
        self.institution_repository = institution_repository

    def execute(self) -> List[Institution]:
        return self.institution_repository.list()


class ListPartiesUseCase:
    def __init__(self, party_repository: IPartyRepository):
        self.party_repository = party_repository

    def execute(self) -> List[Party]:
        return self.party_repository.list()


class ListPeriodsUseCase:
    def __init__(self, period_repository: IPeriodRepository):
        self.period_repository = period_repository

    def execute(self) -> List[Period]:
        return self.period_repository.list()
