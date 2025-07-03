from abc import ABC, abstractmethod
from typing import List
from src.domain.models.common.v_common import UUID
from src.domain.models.context.e_institution import Institution
from src.domain.models.context.e_speaker import Speaker
from src.domain.models.context.e_party import Party

# FIXME: Bloat or not?
class ICountryQueryService(ABC):
    """Query service for retrieving country-related entities."""
    
    @abstractmethod
    def get_institutions_by_country(self, country_id: UUID) -> List[Institution]:
        """Get all institutions for a specific country."""
        pass

    @abstractmethod
    def get_speakers_by_country(self, country_id: UUID) -> List[Speaker]:
        """Get all speakers for a specific country."""
        pass

    @abstractmethod
    def get_parties_by_country(self, country_id: UUID) -> List[Party]:
        """Get all parties for a specific country."""
        pass
    
    @abstractmethod
    def get_speakers_by_party(self, party_id: UUID) -> List[Speaker]:
        """Get all speakers belonging to a specific party."""
        pass
    
    @abstractmethod
    def count_speakers_by_country(self, country_id: UUID) -> int:
        """Get count of speakers for a country without loading all entities."""
        pass
    
    @abstractmethod
    def count_parties_by_country(self, country_id: UUID) -> int:
        """Get count of parties for a country without loading all entities."""
        pass
