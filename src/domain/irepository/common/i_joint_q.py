from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.common.v_enums import InstitutionTypeEnum, CountryEnum
from src.domain.models.common.v_common import UUID\

class IJointQRepository(ABC):
    """Interface for Joint Query Repository."""

    @abstractmethod
    def get_institution_by_country_and_institution_enum(self, 
        country: CountryEnum, 
        institution_enum: InstitutionTypeEnum) -> Optional[Institution]:
        """Get institution by country and institution enum."""
        pass

    @abstractmethod
    def get_country_by_institution_id(self, institution_id: UUID) -> Optional[Country]:
        """Get country by institution ID."""
        pass