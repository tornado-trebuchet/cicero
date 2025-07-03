from src.domain.models.base_model import ValueObject

# TODO: Add format and length validation 
class Label(ValueObject):
    """Represents a naming text"""
    
    def __init__(self, label: str):
        self._label = label

    @property
    def value(self) -> str:
        return self._label

    @value.setter
    def value(self, value: str):
        self._label = value

    def __repr__(self) -> str:
        return f"<Label {self._label}>"