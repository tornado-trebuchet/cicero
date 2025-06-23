from typing import Optional
from datetime import date
from src.domain.models.v_enums import PartyEnum, GenderEnum

class Speaker:
    """Value Object for a speaker (person) in a protocol/speech."""
    def __init__(
        self,
        id: str,
        name: str,
        party: PartyEnum,
        role: str,
        birth_date: Optional[date],
        gender: GenderEnum,
    ):
        self.id = id
        self.name = name
        self.party = party
        self.role = role
        self.birth_date = birth_date
        self.gender = gender

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Speaker)
            and self.id == other.id
            and self.name == other.name
            and self.party == other.party
            and self.role == other.role
            and self.birth_date == other.birth_date
            and self.gender == other.gender
        )

    def __repr__(self) -> str:
        return f"<Speaker {self.name} ({self.party})>"
