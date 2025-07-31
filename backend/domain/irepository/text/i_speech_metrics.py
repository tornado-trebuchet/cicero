from abc import ABC, abstractmethod
from typing import Optional

from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_speech_metrics_plugin import MetricsPlugin


class ISpeechMetricsRepository(ABC):
    """Repository interface for Speech Metrics."""

    @abstractmethod
    def get_by_speech_id(self, speech_id: UUID) -> Optional[MetricsPlugin]:
        """Get speech metrics by speech ID."""
        pass

    @abstractmethod
    def add(self, speech_id: UUID, metrics: MetricsPlugin) -> None:
        """Add speech metrics for a speech."""
        pass

    @abstractmethod
    def update(self, speech_id: UUID, metrics: MetricsPlugin) -> None:
        """Update speech metrics for a speech."""
        pass

    @abstractmethod
    def delete(self, speech_id: UUID) -> None:
        """Delete speech metrics for a speech."""
        pass
