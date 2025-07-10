from typing import Optional, List
from src.domain.models.common.v_common import UUID
from src.domain.models.base_aggregate import AggregateRoot
from src.domain.models.common.v_enums import CountryEnum
# so TODO: domain events
# and think how to ensure speaker deduplication 
class Country(AggregateRoot):
    """Represents a Country in the domain model."""
    def __init__(
        self, 
        id: UUID, 
        country: CountryEnum,
        periodisation: Optional[List[UUID]] = None,
        institutions: Optional[List[UUID]] = None,
        parties: Optional[List[UUID]] = None,
        speakers: Optional[List[UUID]] = None 
    ):
        super().__init__(id)
        self._country = country
        self._periodisation = periodisation if periodisation is not None else []
        self._institutions = institutions if institutions is not None else []
        self._parties = parties if parties is not None else []
        self._speakers = speakers if speakers is not None else []

    @property
    def country(self) -> CountryEnum:
        return self._country

    @property
    def periodisation(self) -> Optional[List[UUID]]:
        return self._periodisation
    
    @periodisation.setter
    def periodisation(self, value: List[UUID]):
        self._periodisation = value
    

    @property
    def institutions(self) -> Optional[List[UUID]]:
        return self._institutions
    
    @institutions.setter
    def institutions(self, value: List[UUID]):
        self._institutions = value

    @property
    def speakers(self) -> Optional[List[UUID]]:
        return self._speakers
    
    @speakers.setter
    def speakers(self, value: List[UUID]):
        self._speakers = value

    def add_speaker(self, speaker: UUID):
        if speaker not in self._speakers:
            self._speakers.append(speaker)

    @property
    def parties(self) -> Optional[List[UUID]]:
        return self._parties
    
    @parties.setter
    def parties(self, value: List[UUID]):
        self._parties = value