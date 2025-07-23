from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import OwnerTypeEnum
from src.domain.models.context.e_period import Period
from src.domain.models.context.v_label import Label


class IPeriodRepository(ABC):
    """Repository interface for Period aggregate."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Period]:
        """Get period by ID."""
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: UUID) -> List[Period]:
        """Get periods by owner ID."""
        pass

    @abstractmethod
    def get_by_owner(self, owner_id: UUID, owner_type: OwnerTypeEnum) -> List[Period]:
        """Get periods by specific owner type and id."""
        pass

    @abstractmethod
    def get_by_label(self, label: Label) -> Optional[Period]:
        """Get period by label."""
        pass

    @abstractmethod
    def list(self) -> List[Period]:
        """List all periods."""
        pass

    @abstractmethod
    def add(self, period: Period) -> None:
        """Add a new period."""
        pass

    @abstractmethod
    def update(self, period: Period) -> None:
        """Update a period."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a period."""
        pass
