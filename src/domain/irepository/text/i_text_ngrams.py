from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_ngrams import NGramizedText


class INGramizedTextRepository(ABC):
    """Repository contract for NGramizedText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[NGramizedText]:
        """Get NGramizedText by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[NGramizedText]:
        """Get NGramizedText by its associated speech_id."""
        pass

    @abstractmethod
    def add(self, ngramized_text: NGramizedText) -> None:
        """Add a new NGramizedText entity."""
        pass

    @abstractmethod
    def update(self, ngramized_text: NGramizedText) -> None:
        """Update an existing NGramizedText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a NGramizedText entity by its unique ID."""
        pass
