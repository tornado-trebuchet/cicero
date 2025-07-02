from typing import List
from src.domain.models.base_model import ValueObject

class TokenizedText(ValueObject):
    
    def __init__(self, tokens: List[str]):
        self._tokens = tokens 

    @property
    def tokens(self) -> List[str]:
        return self._tokens
    
    @tokens.setter
    def tokens(self, value: List[str]):
            self._tokens = value


    def __repr__(self):
        return f"Tokens({self._tokens})"

    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, index: int) -> str:
        return self._tokens[index]
    
    def num_tokens(self) -> int:
        return len(self._tokens)
    
    def unique_token_count(self) -> int:
        return len(set(self._tokens))
