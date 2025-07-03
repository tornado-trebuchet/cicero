from typing import Optional
from src.domain.models.base_model import Entity 
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_label import Label
from src.domain.models.common.v_enums import PartyEnumRegistry
from src.domain.models.context.e_speaker import Speaker

class Party(Entity):
    """Represents a political party"""
    def __init__(
        self, 
        id: UUID,
        country_id: UUID,
        label: Label,
        party_enum: PartyEnumRegistry, # FIXME: That's the problem it should hold the actual enum for a party (probably through party discovery service)
        members: Optional[list[Speaker]] = None,
        party_program: Optional[str] = None # TODO add it's own type 
    ):
        super().__init__(id)
        self._label = label
        self._country_id = country_id
        self._party_enum = party_enum
        self._members = members if members is not None else []
        self._party_program = party_program if party_program is not None else ""
    
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
    def party_enum(self) -> PartyEnumRegistry:
        return self._party_enum
    
    @property
    def members(self) -> Optional[list[Speaker]]:
        return self._members
    
    @members.setter
    def members(self, value: list[Speaker]):
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