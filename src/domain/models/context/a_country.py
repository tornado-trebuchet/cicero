from typing import Optional, List
from src.domain.models.common.v_common import UUID
from src.domain.models.base_model import Entity
from src.domain.models.common.v_enums import CountryEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker

class Country(Entity):
    """Represents a Country in the domain model."""
    def __init__(
        self, 
        id: UUID, 
        country: CountryEnum,
        institutions: Optional[List[Institution]] = None,
        speakers: Optional[List[Speaker]] = None
        ):
        super().__init__(id)
        self._country = country
        self._institutions = institutions if institutions is not None else []
        self._speakers = speakers if speakers is not None else []

    @property
    def country(self) -> CountryEnum:
        return self._country

    @property
    def institutions(self) -> List[Institution]:
        return self._institutions
    
    @institutions.setter
    def institutions(self, value: List[Institution]):
        self._institutions = value

    @property
    def speakers(self) -> List[Speaker]:
        return self._speakers
    
    @speakers.setter
    def speakers(self, value: List[Speaker]):
        self._speakers = value

    def add_speaker(self, speaker: Speaker):
        if speaker not in self._speakers:
            self._speakers.append(speaker)