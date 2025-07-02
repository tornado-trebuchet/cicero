from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import InstitutionTypeEnum

class IInstitutionRepository(ABC):
    """
    Repository for Institution aggregate handling.
    Institution is an aggregate that contains Period value objects within its boundaries.
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        """Get Institution with all its periods."""
        pass
    
    @abstractmethod
    def get_by_id_with_periods(self, id: UUID, include_periods: bool = True) -> Optional[Institution]:
        """Get Institution - periods are always included as part of the aggregate."""
        pass

    @abstractmethod
    def get_by_country_and_type(self, country_id: UUID, institution_type: InstitutionTypeEnum) -> List[Institution]:
        """Get institutions by country and type."""
        pass

    @abstractmethod
    def list(self) -> List[Institution]:
        """List all institutions."""
        pass

    @abstractmethod
    def add(self, institution: Institution) -> None:
        """Add a new institution aggregate."""
        pass

    @abstractmethod
    def update(self, institution: Institution) -> None:
        """Update an institution aggregate."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete an institution aggregate."""
        pass
