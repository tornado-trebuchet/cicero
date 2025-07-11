from src.domain.models.base_vo import ValueObject
from typing import Optional

class TextMetrics(ValueObject):
    def __init__(self):
        self._word_count: Optional[int] = None
        self._character_count: Optional[int] = None
        self._token_count: Optional[int] = None
        self._unique_token_count: Optional[int] = None
        self._sentence_count: Optional[int] = None

    @property
    def word_count(self) -> Optional[int]:
        return self._word_count

    @word_count.setter
    def word_count(self, value: Optional[int]) -> None:
        self._word_count = value

    @property
    def character_count(self) -> Optional[int]:
        return self._character_count

    @character_count.setter
    def character_count(self, value: Optional[int]) -> None:
        self._character_count = value

    @property
    def token_count(self) -> Optional[int]:
        return self._token_count

    @token_count.setter
    def token_count(self, value: Optional[int]) -> None:
        self._token_count = value

    @property
    def unique_token_count(self) -> Optional[int]:
        return self._unique_token_count

    @unique_token_count.setter
    def unique_token_count(self, value: Optional[int]) -> None:
        self._unique_token_count = value

    @property
    def sentence_count(self) -> Optional[int]:
        return self._sentence_count

    @sentence_count.setter
    def sentence_count(self, value: Optional[int]) -> None:
        self._sentence_count = value

