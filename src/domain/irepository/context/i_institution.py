from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum
from src.domain.models.context.v_label import Label
class IInstitutionRepository(ABC):
    """Repository interface for Institution aggregate."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        """Get institution by ID."""
        pass

    @abstractmethod
    def get_by_type(self, institution_type: InstitutionTypeEnum) -> List[Institution]:
        """Get institutions by type (e.g., Parliament, Federal Assembly)."""
        pass
    
    @abstractmethod
    def get_by_label(self, label: Label) -> Optional[Institution]:
        """Get institution by label."""
        pass

    @abstractmethod
    def list(self) -> List[Institution]:
        """List all institutions."""
        pass

    @abstractmethod
    def add(self, institution: Institution) -> None:
        """Add a new institution."""
        pass

    @abstractmethod
    def update(self, institution: Institution) -> None:
        """Update an institution."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete an institution."""
        pass
