from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_tokenized import TokenizedText


class ITokenizedTextRepository(ABC):
    """Repository contract for TokenizedText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[TokenizedText]:
        """Get TokenizedText by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[TokenizedText]:
        """Get TokenizedText by its associated speech_id."""
        pass

    @abstractmethod
    def add(self, tokenized_text: TokenizedText) -> None:
        """Add a new TokenizedText entity."""
        pass

    @abstractmethod
    def update(self, tokenized_text: TokenizedText) -> None:
        """Update an existing TokenizedText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a TokenizedText entity by its unique ID."""
        pass
