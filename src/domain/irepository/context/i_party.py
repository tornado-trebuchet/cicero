from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.e_party import Party
from src.domain.models.common.v_common import UUID
from src.domain.models.context.v_party_name import PartyName

class IPartyRepository(ABC):
    """Repository interface for Party aggregate."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Party]:
        """Get party by ID."""
        pass

    @abstractmethod
    def get_by_name(self, party_name: PartyName) -> Optional[Party]:
        """Get party by name."""
        pass

    @abstractmethod
    def list(self) -> List[Party]:
        """List all parties."""
        pass

    @abstractmethod
    def add(self, party: Party) -> None:
        """Add a new party."""
        pass

    @abstractmethod
    def update(self, party: Party) -> None:
        """Update a party."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a party."""
        pass
