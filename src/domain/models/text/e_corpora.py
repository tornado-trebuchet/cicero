from src.domain.models.text.e_speech import Speech
from src.domain.models.common.base_model import Entity
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum, PartyEnumRegistry, CountryEnum
from typing import Optional

class Corpora(Entity):
    def __init__(
        self,
        id: UUID,
        speech_ids: list[UUID],
        country: Optional[CountryEnum] = None,
        institution: Optional[InstitutionTypeEnum] = None,
        periods: Optional[list[str]] = None,
        party: Optional[PartyEnumRegistry] = None,
    ):
        super().__init__(id)
        self._speech_ids = speech_ids
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
    def speech_ids(self) -> list[UUID]:
        return self._speech_ids

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

    def __repr__(self) -> str:
        return f"<Corpora id={self.id} speeches={len(self._speeches)} institution={self._institution} party={self._party} country={self._country} periods={self._periods}>"

    def properties(self) -> dict:
        return {
            'id': self.id,
            'speech_ids': self._speech_ids,
            'institution': self._institution,
            'party': self._party,
            'country': self._country,
            'period': self._periods,
            'num_speeches': len(self._speeches)
        }

