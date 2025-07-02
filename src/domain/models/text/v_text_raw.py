from src.domain.models.common.base_model import ValueObject

class RawText(ValueObject):

    def __init__(self, text: str):
        self._text = text

    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value if value is not None else ""

    def num_characters(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return self._text
