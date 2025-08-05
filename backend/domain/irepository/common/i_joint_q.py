from abc import ABC, abstractmethod
from typing import Optional, List

from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from backend.domain.models.context.a_country import Country
from backend.domain.models.context.e_institution import Institution
from backend.domain.models.text.a_speech import Speech
from backend.domain.models.text.a_speech_text import SpeechText
from backend.domain.models.text.e_text_raw import RawText
from backend.domain.models.context.e_period import Period
from backend.domain.models.text.a_protocol import Protocol

class IJointQRepository(ABC):
    """Interface for Joint Query Repository."""

    @abstractmethod
    def get_institution_by_country_and_institution_enum(
        self, country: CountryEnum, institution_enum: InstitutionTypeEnum
    ) -> Optional[Institution]:
        """Get institution by country and institution enum."""
        pass

    @abstractmethod
    def get_country_by_institution_id(self, institution_id: UUID) -> Optional[Country]:
        """Get country by institution ID."""
        pass

    @abstractmethod
    def get_protocol_by_speech_id(self, speech_id: UUID) -> Optional[Protocol]:
        """Get protocol by speech ID."""
        pass

    @abstractmethod
    def get_speech_text_by_speech_id(self, speech_id: UUID) -> Optional[SpeechText]:
        """Get speech text by speech ID."""
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