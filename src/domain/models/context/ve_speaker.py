from typing import Optional
from datetime import date
from src.domain.models.common.v_enums import PartyEnumRegistry, GenderEnum
from src.domain.models.common.v_common import UUID
from src.domain.models.common.base_model import Entity

class Speaker(Entity):
    """Value Object (loud, proud and mutable) for a speaker (person) in a protocol/speech."""
    def __init__(
        self,
        id: UUID,
        name: str,
        party: Optional[PartyEnumRegistry] = None,
        role: Optional[str] = None,
        birth_date: Optional[date] = None,
        gender: Optional[GenderEnum] = None,
    ):
        super().__init__(id)
        self._name = name
        self._party = party
        self._role = role
        self._birth_date = birth_date
        self._gender = gender

    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def party(self) -> Optional[PartyEnumRegistry]:
        return self._party

    @party.setter
    def party(self, value: Optional[PartyEnumRegistry]):
        self._party = value

    @property
    def role(self) -> Optional[str]:
        return self._role

    @role.setter
    def role(self, value: Optional[str]):
        self._role = value

    @property
    def birth_date(self) -> Optional[date]:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: Optional[date]):
        self._birth_date = value

    @property
    def gender(self) -> Optional[GenderEnum]:
        return self._gender

    @gender.setter
    def gender(self, value: Optional[GenderEnum]):
        self._gender = value

    def __repr__(self) -> str:
        party_str = str(self._party) if self._party else 'No Party'
        return f"<Speaker {self._name} ({party_str})>"
