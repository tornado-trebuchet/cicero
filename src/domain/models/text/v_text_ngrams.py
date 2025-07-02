from typing import List
from src.domain.models.base_model import ValueObject

class NGramizedText(ValueObject):

    def __init__(self, tokens: List[str]):
        self._tokens = tokens

    @property
    def tokens(self) -> List[str]:
        return self._tokens 

    @tokens.setter
    def tokens(self, value: List[str]):
        self._tokens = value

    def __repr__(self):
        return f"NGramTokens({self.tokens})"

    def __len__(self):
        return len(self.tokens)
