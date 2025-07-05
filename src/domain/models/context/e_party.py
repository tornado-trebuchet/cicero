from typing import Optional
from src.domain.models.base_model import Entity 
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.text.v_party_program_text import PartyProgramText

class Party(Entity):
    """Represents a political party"""
    def __init__(
        self, 
        id: UUID,
        country_id: UUID,
        label: Label,
        members: Optional[list[UUID]] = None,
        party_program: Optional[PartyProgramText] = None
    ):
        super().__init__(id)
        self._label = label
        self._country_id = country_id
        self._members = members
        self._party_program = party_program
    
    @property
    def country_id(self) -> UUID:
        return self._country_id 

    @property
    def label(self) -> Label:
        return self._label
    
    @label.setter
    def label(self, value: Label):
        self._label = value
    
    @property
    def members(self) -> Optional[list[UUID]]:
        return self._members
    
    @members.setter
    def members(self, value: list[UUID]):
        self._members = value
    
    @property
    def party_program(self) -> Optional[str]:
        return self._party_program
    
    @party_program.setter  
    def party_program(self, value: Optional[str]):
        self._party_program = value
    
    def add_member(self, speaker: Speaker):
        """Add a speaker to the party members."""
        if speaker not in self._members:
            self._members.append(speaker)
    
    def remove_member(self, speaker: Speaker):
        """Remove a speaker from the party members."""
        if speaker in self._members:
            self._members.remove(speaker)
    
    def __repr__(self) -> str:
        return f"<Party {self._label} ({self._country_id})>"