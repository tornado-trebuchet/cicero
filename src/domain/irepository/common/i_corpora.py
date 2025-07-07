from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.common.a_corpora import Corpora
from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum
from src.domain.models.context.v_label import Label

class ICorporaRepository(ABC):
    """Repository contract for Corpora aggregates."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Corpora]:
        """Get a Corpora aggregate by its unique ID."""
        pass

    def get_by_label(self, label: Label) -> Optional[Corpora]:
        """Get a Corpora aggregate by its label."""
        pass

    @abstractmethod
    def list_by_country(self, country: CountryEnum) -> List[Corpora]:
        """List all Corpora aggregates for a given country."""
        pass

    @abstractmethod
    def add(self, corpora: Corpora) -> None:
        """Add a new Corpora aggregate to the repository."""
        pass

    @abstractmethod
    def remove(self, id: UUID) -> None:
        """Remove a Corpora aggregate by its unique ID."""
        pass

    @abstractmethod
    def update(self, corpora: Corpora) -> None:
        """Update an existing Corpora aggregate."""
        pass
