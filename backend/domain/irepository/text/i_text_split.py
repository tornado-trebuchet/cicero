from abc import ABC, abstractmethod
from typing import Optional

from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_text_split import TextSentences


class ITextSentencesRepository(ABC):
    """Repository contract for TextSentences entity handling."""

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[TextSentences]:
        """Get TextSentences by its unique ID."""
        pass

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[TextSentences]:
        """Get TextSentences by its associated speech_id."""
        pass

    @abstractmethod
    def add(self, text_sentences: TextSentences) -> None:
        """Add a new TextSentences entity."""
        pass

    @abstractmethod
    def update(self, text_sentences: TextSentences) -> None:
        """Update an existing TextSentences entity."""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a TextSentences entity by its unique ID."""
        pass
