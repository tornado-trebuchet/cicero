class RawText:

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

    def __repr__(self) -> str:
        return f"RawText(text={self._text!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RawText):
            return NotImplemented
        return self._text == other._text
