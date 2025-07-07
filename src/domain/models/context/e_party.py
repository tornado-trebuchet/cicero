from typing import Optional
from src.domain.models.base_model import Entity 
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_party_name import PartyName
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.text.v_party_program_text import PartyProgramText

class Party(Entity):
    """Represents a political party"""
    def __init__(
        self, 
        id: UUID,
        country_id: UUID,
        party_name: PartyName,
        party_program: Optional[PartyProgramText] = None,
        speakers: Optional[list[Speaker]] = None
    ):
        super().__init__(id)
        self._party_name = party_name
        self._country_id = country_id
        self._party_program = party_program
        self._speakers = speakers if speakers is not None else []
    
    @property
    def country_id(self) -> UUID:
        return self._country_id 

    @property
    def party_name(self) -> PartyName:
        return self._party_name
    
    @party_name.setter
    def party_name(self, value: PartyName):
        self._party_name = value
    
    @property
    def speakers(self) -> Optional[list[Speaker]]:
        return self._speakers
    
    @speakers.setter
    def speakers(self, value: list[Speaker]):
        self._speakers = value
    
    @property
    def party_program(self) -> Optional[PartyProgramText]:
        return self._party_program
    
    @party_program.setter  
    def party_program(self, value: Optional[PartyProgramText]):
        self._party_program = value
    
    def add_member(self, speaker: Speaker):
        """Add a speaker to the party speakers."""
        if speaker not in self._speakers:
            self._speakers.append(speaker)
    
    def remove_member(self, speaker: Speaker):
        """Remove a speaker from the party speakers."""
        if speaker in self._speakers:
            self._speakers.remove(speaker)
    
    def __repr__(self) -> str:
        return f"<Party {self._party_name} ({self._country_id})>"