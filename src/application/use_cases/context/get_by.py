from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from src.infrastructure.repository.pgsql.context.rep_institution import InstitutionRepository
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.common.v_common import UUID

class GetCountryByIdUseCase:
    def __init__(self):
        self.country_repo = CountryRepository()

    def execute(self, country_id: UUID):
        return self.country_repo.get_by_id(country_id)

class GetInstitutionByIdUseCase:
    def __init__(self):
        self.institution_repo = InstitutionRepository()

    def execute(self, institution_id: UUID):
        return self.institution_repo.get_by_id(institution_id)

class GetCountryByEnumUseCase:
    def __init__(self):
        self.country_repo = CountryRepository()

    def execute(self, country_enum: CountryEnum):
        return self.country_repo.get_by_country_enum(country_enum)

class GetInstitutionsByTypeUseCase:
    def __init__(self):
        self.institution_repo = InstitutionRepository()

    def execute(self, institution_type: InstitutionTypeEnum):
        return self.institution_repo.get_by_type(institution_type)
