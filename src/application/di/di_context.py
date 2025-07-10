from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from src.application.use_cases.context.list import ListCountriesUseCase, ListInstitutionsUseCase
from src.application.use_cases.context.get_by import GetCountryByIdUseCase, GetInstitutionByIdUseCase
from src.application.use_cases.context.get_by import GetCountryByEnumUseCase, GetInstitutionsByTypeUseCase

def get_country_repository():
    return CountryRepository()

def get_institution_repository():
    return InstitutionRepository()

def get_list_countries_use_case():
    return ListCountriesUseCase(get_country_repository())

def get_country_by_id_use_case():
    return GetCountryByIdUseCase()

def get_institution_by_id_use_case():
    return GetInstitutionByIdUseCase()

def get_country_by_enum_use_case():
    return GetCountryByEnumUseCase()

def get_institutions_by_type_use_case():
    return GetInstitutionsByTypeUseCase()

def get_list_institutions_use_case():
    return ListInstitutionsUseCase(get_institution_repository())

