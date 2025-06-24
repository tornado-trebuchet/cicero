from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.e_protocol import Protocol
from src.domain.models.v_common import UUID

class IProtocolRepository(ABC):
    """
    Repository for Protocol entity handling.
    Protocol references but does not own Period (Period belongs to Institution aggregate).
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Protocol]:
        """Get protocol by ID."""
        pass

    @abstractmethod
    def get_by_institution_id(self, institution_id: UUID) -> List[Protocol]:
        """Get all protocols for an institution."""
        pass
        
    @abstractmethod
    def get_by_institution_and_period(self, institution_id: UUID, period_id: UUID) -> List[Protocol]:
        """Get protocols for a specific institution and period."""
        pass
        
    @abstractmethod
    def get_by_date_range(self, start_date, end_date) -> List[Protocol]:
        """Get protocols within a date range."""
        pass

    @abstractmethod
    def list(self) -> List[Protocol]:
        """List all protocols."""
        pass

    @abstractmethod
    def add(self, protocol: Protocol) -> None:
        """Add a new protocol."""
        pass

    @abstractmethod
    def update(self, protocol: Protocol) -> None:
        """Update a protocol."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a protocol (will cascade delete speeches)."""
        pass
