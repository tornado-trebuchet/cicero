from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_clean import CleanText


class ICleanTextRepository(ABC):
    """Repository contract for CleanText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[CleanText]:
        """Get CleanText by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[CleanText]:
        """Get CleanText by its associated speech_id."""
        pass

    @abstractmethod
    def get_by_speech_ids(self, speech_ids: List[UUID]) -> List[str]:
        """Get clean texts for a list of speech IDs."""
        pass

    @abstractmethod
    def add(self, clean_text: CleanText) -> None:
        """Add a new CleanText entity."""
        pass

    @abstractmethod
    def update(self, clean_text: CleanText) -> None:
        """Update an existing CleanText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a CleanText entity by its unique ID."""
        pass
