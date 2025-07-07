from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.text.a_speech import Speech
from domain.models.common.v_common import UUID
from domain.models.context.e_period import Period

class ISpeechRepository(ABC):
    """Speech links text and author"""
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Speech]:
        pass

    @abstractmethod
    def get_by_protocol_id(self, protocol_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_speaker_id(self, speaker_id: UUID) -> List[Speech]:
        pass

    @abstractmethod
    def get_by_date_range(self, start_date, end_date) -> List[Speech]:
        """Get all speeches whose protocol date is within the given range."""
        pass

    @abstractmethod
    def get_by_period(self, period_id: Period) -> List[Speech]:
        """Get all speeches for a given period (via protocol's period_id)."""
        pass

    @abstractmethod
    def list(self) -> List[Speech]:
        pass

    @abstractmethod
    def add(self, speech: Speech) -> None:
        pass

    @abstractmethod
    def update(self, speech: Speech) -> None:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

