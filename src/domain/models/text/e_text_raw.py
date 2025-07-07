from src.domain.models.base_model import Entity
from src.domain.models.common.v_common import UUID

class RawText(Entity):

    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        text: str
    ):
        self._text = text
        self._speech_id = speech_id
        super().__init__(id)
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def speech_id(self) -> UUID:
        return self._speech_id

    def num_characters(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"<RawText id={self.id} speech_id={self.speech_id} text='{self.text[:30]}...'>"
