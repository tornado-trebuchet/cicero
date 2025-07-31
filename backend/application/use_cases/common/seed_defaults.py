from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from backend.domain.models.context.a_country import Country
from backend.domain.models.context.e_institution import Institution
from backend.domain.models.context.v_label import Label
from backend.infrastructure.repository.pgsql.context.rep_country import (
    CountryRepository,
)
from backend.infrastructure.repository.pgsql.context.rep_institution import (
    InstitutionRepository,
)


class SeedDefaultsUseCase:
    def __init__(self):
        self.country_repo = CountryRepository()
        self.institution_repo = InstitutionRepository()

    def seed_countries(self):
        for country_enum in CountryEnum:
            if self.country_repo.get_by_country_enum(country_enum):
                continue
            country = Country(id=UUID.new(), country=country_enum)
            self.country_repo.add(country)

    def seed_institutions(self):
        for country_enum in CountryEnum:
            country = self.country_repo.get_by_country_enum(country_enum)
            if not country:
                continue
            for institution_type in InstitutionTypeEnum:
                all_institutions = self.institution_repo.list()
                existing = [
                    inst
                    for inst in all_institutions
                    if inst.country_id == country.id and inst.type == institution_type
                ]
                if existing:
                    continue
                institution = Institution(
                    id=UUID.new(),
                    country_id=country.id,
                    type=institution_type,
                    label=Label(f"{institution_type.value} of {country_enum.value}"),
                )
                self.institution_repo.add(institution)

    def execute(self):
        self.seed_countries()
        self.seed_institutions()
