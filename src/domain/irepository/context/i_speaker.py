from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_name import Name

class ISpeakerRepository(ABC):
    """Repository interface for Speaker aggregate."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Speaker]:
        """Get speaker by ID."""
        pass

    @abstractmethod
    def get_by_name(self, name: Name) -> List[Speaker]:
        """Get speakers by name."""
        pass

    @abstractmethod
    def list(self) -> List[Speaker]:
        """List all speakers."""
        pass

    @abstractmethod
    def add(self, speaker: Speaker) -> None:
        """Add a new speaker."""
        pass

    @abstractmethod
    def update(self, speaker: Speaker) -> None:
        """Update a speaker."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a speaker."""
        pass
