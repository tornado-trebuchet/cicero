from src.domain.models.base_model import ValueObject

class TextMetrics(ValueObject):
    word_count: int
    character_count: int
    token_count: int
    unique_token_count: int
    sentence_count: int

@property
def word_count(self) -> int:
    return self._word_count

@word_count.setter
def word_count(self, value: int):
    self._word_count = value

@property
def character_count(self) -> int:
    return self._character_count

@character_count.setter
def character_count(self, value: int):
    self._character_count = value

@property
def token_count(self) -> int:
    return self._token_count

@token_count.setter
def token_count(self, value: int):
    self._token_count = value

@property
def unique_token_count(self) -> int:
    return self._unique_token_count

@unique_token_count.setter
def unique_token_count(self, value: int):
    self._unique_token_count = value

@property
def sentence_count(self) -> int:
    return self._sentence_count

@sentence_count.setter
def sentence_count(self, value: int):
    self._sentence_count = value

