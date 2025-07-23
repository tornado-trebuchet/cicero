from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.e_text_raw import RawText
from src.domain.models.context.e_period import Period

class IJointQRepository(ABC):
    """Interface for Joint Query Repository."""

    @abstractmethod
    def get_institution_by_country_and_institution_enum(
        self, country: CountryEnum, institution_enum: InstitutionTypeEnum
    ) -> Optional[Institution]:
        """Get institution by country and institution enum."""
        pass

    @abstractmethod
    def get_country_by_institution_id(
        self, institution_id: UUID
    ) -> Optional[Country]:
        """Get country by institution ID."""
        pass

    @abstractmethod
    def add_speech_speech_text_and_raw_text(
        self, speech: Speech, speech_text: SpeechText, raw_text: RawText
    ) -> None:
        """Add speech, speech text, and raw text to the repository."""
        pass

    @abstractmethod
    def get_speeches_with_filter(
        self,
        countries: Optional[List[UUID]] = None,
        institutions: Optional[List[UUID]] = None,
        protocols: Optional[List[UUID]] = None,
        party_ids: Optional[List[UUID]] = None,
        speaker_ids: Optional[List[UUID]] = None,
        periods: Optional[List[Period]] = None,
    ) -> list[Speech]:
        """Get speeches with optional filters"""
        pass