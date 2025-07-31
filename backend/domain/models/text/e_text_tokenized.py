from typing import List

from backend.domain.models.base_entity import Entity
from backend.domain.models.common.v_common import UUID


class TokenizedText(Entity):

    def __init__(self, id: UUID, speech_text_id: UUID, tokens: List[str]):
        self._tokens = tokens
        self._speech_text_id = speech_text_id
        super().__init__(id)

    @property
    def tokens(self) -> List[str]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: List[str]):
        self._tokens = value

    @property
    def speech_text_id(self) -> UUID:
        return self._speech_text_id

    def __repr__(self):
        return f"Tokens(id={self.id}, speech_id={self.speech_text_id}, tokens={self._tokens})"

    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, index: int) -> str:
        return self._tokens[index]

    def num_tokens(self) -> int:
        return len(self._tokens)

    def unique_token_count(self) -> int:
        return len(set(self._tokens))
