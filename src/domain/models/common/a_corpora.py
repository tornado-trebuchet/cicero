from src.domain.models.text.a_speech import Speech
from src.domain.models.common.base_model import AggregateRoot
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum, PartyEnumRegistry, CountryEnum
from typing import Optional

class Corpora(AggregateRoot):
    def __init__(
        self,
        id: UUID,
        speeches: list[Speech],
        country: CountryEnum,
        institution: InstitutionTypeEnum,
        periods: Optional[list[str]] = None,
        party: Optional[PartyEnumRegistry] = None,
    ):
        super().__init__(id)
        self._speeches = speeches
        self._institution = institution
        self._party = party
        self._country = country
        self._periods = periods if periods is not None else []

    @property
    def speeches(self) -> list['Speech']:
        return self._speeches

    @speeches.setter
    def speeches(self, value: list['Speech']):
        self._speeches = value

    @property
    def speech_ids(self) -> list[Speech]:
        return self._speeches

    @property
    def institution(self) -> Optional[InstitutionTypeEnum]:
        return self._institution

    @property
    def party(self) -> Optional[PartyEnumRegistry]:
        return self._party

    @property
    def country(self) -> Optional[CountryEnum]:
        return self._country

    @property
    def periods(self) -> Optional[list[str]]:
        return self._periods

    def __len__(self) -> int:
        return len(self._speeches)
