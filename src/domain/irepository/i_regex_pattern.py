from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.e_regex_pattern import RegexPattern
from src.domain.models.v_common import UUID

class IRegexPatternRepository(ABC):
    """
    Repository for RegexPattern entity handling.
    RegexPattern references Country, Institution, and optionally Period but doesn't own them.
    """
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[RegexPattern]:
        """Get regex pattern by ID."""
        pass

    @abstractmethod
    def get_active_by_scope(self, country_id: UUID, institution_id: UUID, period_id: Optional[UUID] = None) -> List[RegexPattern]:
        """Get active regex patterns for a specific scope (country, institution, optional period)."""
        pass
        
    @abstractmethod
    def get_by_country_and_institution(self, country_id: UUID, institution_id: UUID) -> List[RegexPattern]:
        """Get all regex patterns for a country and institution."""
        pass
        
    @abstractmethod
    def get_latest_version_by_scope(self, country_id: UUID, institution_id: UUID, period_id: Optional[UUID] = None) -> Optional[RegexPattern]:
        """Get the latest version of regex pattern for a scope."""
        pass

    @abstractmethod
    def list(self) -> List[RegexPattern]:
        """List all regex patterns."""
        pass

    @abstractmethod
    def add(self, regex_pattern: RegexPattern) -> None:
        """Add a new regex pattern."""
        pass

    @abstractmethod
    def update(self, regex_pattern: RegexPattern) -> None:
        """Update a regex pattern."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a regex pattern."""
        pass
