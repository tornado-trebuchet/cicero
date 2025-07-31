from backend.domain.models.base_vo import ValueObject


# TODO: Add format and length validation
class Name(ValueObject):
    """Name of a speaker"""

    def __init__(self, name: str):
        self._name = name

    @property
    def value(self) -> str:
        return self._name

    @value.setter
    def value(self, value: str):
        self._name = value

    def __repr__(self) -> str:
        return f"<Name {self._name}>"
