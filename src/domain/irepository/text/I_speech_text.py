from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.common.v_common import UUID

class ISpeechTextRepository(ABC):
    """Repository for SpeechText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[SpeechText]:
        """Get SpeechText by its unique ID."""
        pass

    @abstractmethod
    def add(self, speech_text: SpeechText) -> None:
        """Add a new SpeechText entity."""
        pass

    @abstractmethod
    def update(self, speech_text: SpeechText) -> None:
        """Update an existing SpeechText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a SpeechText entity by its unique ID."""
        pass

