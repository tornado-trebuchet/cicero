from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.context.e_institution import Institution
from domain.models.context.ve_period import Period
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import InstitutionTypeEnum

class IInstitutionRepository(ABC):
    """
    Repository for Institution aggregate handling.
    Institution is an aggregate that contains Period entities within its boundaries.
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Institution]:
        """Get fully rehydrated Institution with all its periods."""
        pass
    
    @abstractmethod
    def get_by_id_with_periods(self, id: UUID, include_periods: bool = True) -> Optional[Institution]:
        """Get Institution with optional period loading for performance."""
        pass

    @abstractmethod
    def get_by_country_and_type(self, country_id: UUID, institution_type: InstitutionTypeEnum) -> List[Institution]:
        """Get institutions by country and type with periods."""
        pass

    @abstractmethod
    def list(self) -> List[Institution]:
        """List all institutions with their periods."""
        pass

    @abstractmethod
    def add(self, institution: Institution) -> None:
        """
        Add a new institution aggregate.
        Will persist Institution and all its Period entities as a transaction.
        """
        pass

    @abstractmethod
    def update(self, institution: Institution) -> None:
        """
        Update an institution aggregate.
        Will update Institution and sync its Period entities.
        """
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """
        Delete an institution aggregate.
        Will cascade delete all contained periods.
        """
        pass
        
    @abstractmethod
    def add_period_to_institution(self, institution_id: UUID, period: Period) -> None:
        """Add a new period to an existing institution."""
        pass
        
    @abstractmethod
    def remove_period_from_institution(self, institution_id: UUID, period_id: UUID) -> None:
        """Remove a period from an institution."""
        pass
