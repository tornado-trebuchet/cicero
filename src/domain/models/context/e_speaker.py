from typing import Optional, List
from src.domain.models.base_entity import Entity
from src.domain.models.common.v_common import DateTime
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import GenderEnum
from src.domain.models.context.v_name import Name

class Speaker(Entity):
    """Speaker references it's speeches, belongs to a country and sometimes party"""
    def __init__(
        self,
        id: UUID,
        country_id: UUID,
        name: Name,
        speeches: Optional[List[UUID]] = None,
        party: Optional[UUID] = None,
        role: Optional[str] = None,
        birth_date: Optional[DateTime] = None,
        gender: Optional[GenderEnum] = None,
    ):
        super().__init__(id)
        self._country_id = country_id
        self._name = name
        self._speeches = speeches
        self._party = party
        self._role = role
        self._birth_date = birth_date
        self._gender = gender

    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def country_id(self) -> UUID:
        return self._country_id

    @property
    def name(self) -> Name:
        return self._name

    @name.setter
    def name(self, value: Name):
        self._name = value

    @property
    def speeches(self) -> Optional[List[UUID]]:
        return self._speeches
    
    @speeches.setter
    def speeches(self, value: List[UUID]):
        self._speeches = value

    @property
    def party(self) -> Optional[UUID]:
        return self._party

    @party.setter
    def party(self, value: Optional[UUID]):
        self._party = value

    @property
    def role(self) -> Optional[str]:
        return self._role

    @role.setter
    def role(self, value: Optional[str]):
        self._role = value

    @property
    def birth_date(self) -> Optional[DateTime]:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: Optional[DateTime]):
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
