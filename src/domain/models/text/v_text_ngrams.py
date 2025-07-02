from typing import Optional, List
from src.domain.models.common.base_model import ValueObject

class NGramTokens(ValueObject):

    def __init__(self, tokens: Optional[List[str]] = None):
        self._tokens = tokens if tokens is not None else []

    def __repr__(self):
        return f"NGramTokens({self.tokens})"

    def __len__(self):
        return len(self.tokens)
    
    @property
    def tokens(self) -> List[str]:
        return self._tokens 

    @tokens.setter
    def tokens(self, value: List[str]):
        self._tokens = value