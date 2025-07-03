from typing import Optional, List
from src.domain.models.common.v_common import UUID
from src.domain.models.base_model import AggregateRoot
from src.domain.models.common.v_enums import CountryEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party

# TODO: Switch to using IDs for enforcing invariants
# e.g. Many parsed parties should be unified under enums and checked against it
# or normalisation of speakers 
# speaker - to many institutions relationship while updating 
# so TODO: domain events 
class Country(AggregateRoot):
    """Represents a Country in the domain model."""
    def __init__(
        self, 
        id: UUID, 
        country: CountryEnum,
        institutions: Optional[List[Institution]] = None,
        speakers: Optional[List[Speaker]] = None, 
        parties: Optional[List[Party]] = None
    ):
        super().__init__(id)
        self._country = country
        self._institutions = institutions if institutions is not None else []
        self._speakers = speakers if speakers is not None else []
        self._parties = parties if parties is not None else []
    @property
    def country(self) -> CountryEnum:
        return self._country

    @property
    def institutions(self) -> Optional[List[Institution]]:
        return self._institutions
    
    @institutions.setter
    def institutions(self, value: List[Institution]):
        self._institutions = value

    @property
    def speakers(self) -> Optional[List[Speaker]]:
        return self._speakers
    
    @speakers.setter
    def speakers(self, value: List[Speaker]):
        self._speakers = value

    def add_speaker(self, speaker: Speaker):
        if speaker not in self._speakers:
            self._speakers.append(speaker)