from src.domain.models.v_common import UUID
from src.domain.models.base_model import Entity
from src.domain.models.v_enums import CountryEnum

class Country(Entity):
    """
    Represents a Country in the domain model.
    """
    def __init__(self, id: UUID, country: CountryEnum):
        super().__init__(id)
        self._country = country

    @property
    def country(self) -> CountryEnum:
        return self._country

    def __repr__(self) -> str:
        return f"<Country {self._country} {self.id}>"
