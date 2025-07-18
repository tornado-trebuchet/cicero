from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.common.v_common import UUID
from src.domain.models.common.v_enums import CountryEnum, InstitutionTypeEnum
from src.domain.models.context.a_country import Country
from src.domain.models.context.e_institution import Institution
from src.domain.models.text.a_speech import Speech
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.e_text_raw import RawText


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
