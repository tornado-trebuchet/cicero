import re
import string

from backend.domain.models.base_entity import Entity
from backend.domain.models.common.v_common import UUID


class CleanText(Entity):

    def __init__(self, id: UUID, speech_text_id: UUID, text: str):
        self._text = text
        self._speech_text_id = speech_text_id
        super().__init__(id)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @property
    def speech_text_id(self) -> UUID:
        return self._speech_text_id

    def num_words(self) -> int:
        return len(self._text.split())

    def num_characters(self, include_whitespace: bool = True, include_punctuation: bool = True) -> int:
        if not include_whitespace:
            text = "".join(self._text.split())
        else:
            text = self._text

        if not include_punctuation:
            text = text.translate(str.maketrans("", "", string.punctuation))

        return len(text)

    def num_sentences(self) -> int:
        sentences = re.split(r"[.!?]+", self.text)
        return len([s for s in sentences if s.strip()])

    def split_sentences(self) -> list[str]:
        sentences = re.split(r"[.!?]+", self.text)
        return [s.strip() for s in sentences if s.strip()]

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<CleanText id={self.id} speech_id={self.speech_text_id} text='{self.text[:30]}...'>"
