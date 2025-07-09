from src.domain.models.context.a_country import Country
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.infrastructure.repository.pgsql.context.rep_country import CountryRepository
from typing import Optional, List

class CreateCountryUseCase:
    def __init__(self):
        self.repository = CountryRepository()

    def execute(self, id: UUID, country: CountryEnum, periodisation: Optional[List[UUID]] = None, institutions: Optional[List[UUID]] = None, parties: Optional[List[UUID]] = None, speakers: Optional[List[UUID]] = None):
        country_obj = Country(
            id=id,
            country=country,
            periodisation=periodisation,
            institutions=institutions,
            parties=parties,
            speakers=speakers
        )
        self.repository.add(country_obj)
        return country_obj
