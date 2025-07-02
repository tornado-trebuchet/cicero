from typing import Optional
from src.domain.models.base_model import ValueObject

class SpeechSentences(ValueObject):
    def __init__(self, sentences: list[str]):
        self._sentences = sentences

    @property
    def sentences(self) -> Optional[list[str]]:
        return self._sentences

    @sentences.setter
    def sentences(self, value: list[str]):
        self._sentences = value

    def __len__(self) -> int:
        return len(self._sentences) if self._sentences is not None else 0