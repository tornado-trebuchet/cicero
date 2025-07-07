from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.text.e_text_translated import TranslatedText
from src.domain.models.common.v_common import UUID

class ITranslatedTextRepository(ABC):
    """Repository contract for TranslatedText entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[TranslatedText]:
        """Get TranslatedText by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[TranslatedText]:
        """Get TranslatedText by its associated speech_id."""
        pass

    @abstractmethod
    def add(self, translated_text: TranslatedText) -> None:
        """Add a new TranslatedText entity."""
        pass

    @abstractmethod
    def update(self, translated_text: TranslatedText) -> None:
        """Update an existing TranslatedText entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a TranslatedText entity by its unique ID."""
        pass
