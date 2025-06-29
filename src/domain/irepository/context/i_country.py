from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.context.e_country import Country
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import CountryEnum

class ICountryRepository(ABC):
    """
    Repository for Country entity handling.
    Country is a simple entity without complex aggregates.
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Country]:
        """Get country by ID."""
        pass
        
    @abstractmethod
    def get_by_country_enum(self, country: CountryEnum) -> Optional[Country]:
        """Get country by country enum value."""
        pass

    @abstractmethod
    def list(self) -> List[Country]:
        """List all countries."""
        pass

    @abstractmethod
    def add(self, country: Country) -> None:
        """Add a new country."""
        pass

    @abstractmethod
    def update(self, country: Country) -> None:
        """Update a country."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a country (will cascade delete institutions)."""
        pass
