from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.common.v_common import UUID

class ISpeakerRepository(ABC):
    """
    Repository contract for Speaker aggregate handling.
    Speaker is a domain entity representing a person in a protocol/speech.
    """

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Speaker]:
        """Get a fully rehydrated Speaker by id."""
        pass

    @abstractmethod
    def list(self) -> List[Speaker]:
        """List all speakers."""
        pass

    @abstractmethod
    def add(self, speaker: Speaker) -> None:
        """Add a new speaker aggregate."""
        pass

    @abstractmethod
    def update(self, speaker: Speaker) -> None:
        """Update an existing speaker aggregate."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a speaker aggregate by id."""
        pass
