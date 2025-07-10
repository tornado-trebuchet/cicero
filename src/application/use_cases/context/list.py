from typing import List
from src.domain.irepository.context.i_country import ICountryRepository
from src.domain.models.context.a_country import Country
from src.domain.irepository.context.i_institution import IInstitutionRepository
from src.domain.models.context.e_institution import Institution

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
