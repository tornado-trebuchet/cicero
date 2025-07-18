from src.domain.models.base_entity import Entity
from src.domain.models.common.v_common import UUID


class TextSentences(Entity):
    def __init__(self, id: UUID, speech_text_id: UUID, sentences: list[str]):
        self._sentences = sentences
        self._speech_text_id = speech_text_id
        super().__init__(id)

    @property
    def sentences(self) -> list[str]:
        return self._sentences

    @sentences.setter
    def sentences(self, value: list[str]):
        self._sentences = value

    @property
    def speech_text_id(self) -> UUID:
        return self._speech_text_id

    def __len__(self) -> int:
        return len(self._sentences)

    def __repr__(self) -> str:
        return f"<TextSentences id={self.id} speech_id={self.speech_text_id} sentences={len(self._sentences)} >"
