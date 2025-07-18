from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.text.e_text_raw import RawText


class IRawTextRepository(ABC):
    """Repository contract for RawText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[RawText]:
        """Get RawText by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[RawText]:
        """Get RawText by its associated speech_id."""
        pass

    @abstractmethod
    def add(self, raw_text: RawText) -> None:
        """Add a new RawText entity."""
        pass

    @abstractmethod
    def update(self, raw_text: RawText) -> None:
        """Update an existing RawText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a RawText entity by its unique ID."""
        pass
