from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.text.a_speech import Speech
from domain.models.common.v_common import UUID

class ISpeechRepository(ABC):
    """
    Repository for Speech aggregate handling.
    Speech is an aggregate that requires full rehydration with Speaker and Text entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        """Get fully rehydrated Speech with Speaker and Text entities."""
        pass

    @abstractmethod
    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        """Get all fully rehydrated speeches for a protocol."""
        pass

    @abstractmethod
    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        """Get all fully rehydrated speeches by a specific speaker."""
        pass

    @abstractmethod
    def list(self) -> List[Speech]:
        """List all fully rehydrated speeches."""
        pass

    @abstractmethod
    def add(self, speech: Speech) -> None:
        """
        Add a new speech aggregate.
        Will persist Speech, Speaker, and Text entities as a transaction.
        """
        pass

    @abstractmethod
    def update(self, speech: Speech) -> None:
        """
        Update a speech aggregate.
        Will update Speech, Speaker, and Text entities as needed.
        """
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """
        Delete a speech aggregate.
        Will cascade delete Text but preserve Speaker for other speeches.
        """
        pass

    @abstractmethod
    def get_by_date_range(self, start_date, end_date) -> List[Speech]:
        """Get all speeches whose protocol date is within the given range."""
        pass

    @abstractmethod
    def get_by_period(self, period_id: UUID) -> List[Speech]:
        """Get all speeches for a given period (via protocol's period_id)."""
        pass
