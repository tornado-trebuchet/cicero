from typing import List
from domain.models.base_vo import Entity
from src.domain.models.common.v_common import UUID

class NGramizedText(Entity):

    def __init__(
        self,
        id: UUID,
        speech_id: UUID,
        tokens: List[str]
    ):
        self._tokens = tokens
        self._speech_id = speech_id
        super().__init__(id)
    
    @property
    def tokens(self) -> List[str]:
        return self._tokens 

    @tokens.setter
    def tokens(self, value: List[str]):
        self._tokens = value

    @property
    def speech_id(self) -> UUID:
        return self._speech_id

    def __repr__(self):
        return f"NGramTokens(id={self.id}, speech_id={self.speech_id}, tokens={self.tokens})"

    def __len__(self):
        return len(self.tokens)
