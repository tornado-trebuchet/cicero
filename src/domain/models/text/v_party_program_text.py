from src.domain.models.base_model import ValueObject

class PartyProgramText(ValueObject):
    """Represents the text of a party program as a value object."""

    def __init__(self, program_text: str):
        self._program_text = program_text

    def __repr__(self):
        return f"PartyProgramText({self._program_text})"

    @property
    def program_text(self) -> str:
        return self._program_text

    @program_text.setter
    def program_text(self, value: str):
        self._program_text = value
