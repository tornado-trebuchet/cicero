from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.context.a_country import Country
from domain.models.common.v_common import UUID
from domain.models.common.v_enums import CountryEnum
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party


# TODO: Allign with domain 
class ICountryRepository(ABC):
    """
    Repository for Country entity handling.
    Holds and offers interface to work with Speakers,Parties and Institutions
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

    @abstractmethod
    def get_institutions(self, country_id: UUID) -> List[Institution]:
        """Get institutions for a specific country."""
        pass

    @abstractmethod
    def get_speakers(self, country_id: UUID) -> List[Speaker]:
        """Get speakers for a specific country."""
        pass

    @abstractmethod
    def get_parties(self, country_id: UUID) -> List[Party]:
        """Get parties for a specific country."""
        pass