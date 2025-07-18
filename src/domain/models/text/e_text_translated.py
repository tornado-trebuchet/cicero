from src.domain.models.base_entity import Entity
from src.domain.models.common.v_common import UUID


class TranslatedText(Entity):
    """Value object for translated text to english"""

    def __init__(self, id: UUID, speech_text_id: UUID, translated_text: str):
        self._translated_text = translated_text
        self._speech_text_id = speech_text_id
        super().__init__(id)

    @property
    def translation(self) -> str:
        return self._translated_text

    @translation.setter
    def translation(self, value: str):
        self._translated_text = value

    @property
    def speech_text_id(self) -> UUID:
        return self._speech_text_id

    def __repr__(self) -> str:
        return f"<TranslatedText id={self.id} speech_id={self.speech_text_id} text='{self._translated_text[:30]}...'>"
