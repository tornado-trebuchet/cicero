from typing import Optional
from src.domain.models.common.v_common import UUID
from src.domain.models.base_model import Entity
from src.domain.models.text.a_speech_text import SpeechText
from src.domain.models.text.v_speech_metrics_plugin import MetricsPlugin
from src.domain.models.common.v_metadata_plugin import MetadataPlugin

class Speech(Entity):
    """Represents a speech in a protocol"""
    def __init__(
        self,
        id: UUID,
        protocol_id: UUID,
        speaker_id: UUID,
        text: SpeechText,
        metadata: Optional[MetadataPlugin] = None,
        metrics: Optional[MetricsPlugin] = None,
    ):
        super().__init__(id)
        self._protocol_id = protocol_id
        self._speaker_id = speaker_id
        self._text = text
        self._metrics = metrics
        self._metadata = metadata

    @property
    def protocol_id(self) -> UUID:
        return self._protocol_id

    @protocol_id.setter
    def protocol_id(self, value: UUID):
        self._protocol_id = value

    @property
    def speaker_id(self) -> UUID:
        return self._speaker_id

    @speaker_id.setter
    def speaker_id(self, value: UUID):
        self._speaker_id = value

    @property
    def text(self) -> SpeechText:
        return self._text

    @text.setter
    def text(self, value: SpeechText):
        self._text = value

    @property
    def metrics(self) -> Optional[MetricsPlugin]:
        return self._metrics

    @metrics.setter
    def metrics(self, value: Optional[MetricsPlugin]):
        self._metrics = value

    @property
    def metadata(self) -> Optional[MetadataPlugin]:
        return self._metadata

    @metadata.setter
    def metadata(self, value: MetadataPlugin):
        self._metadata = value if value is not None else MetadataPlugin({})

    def __repr__(self) -> str:
        return f"<Speech {self.id} by {self._speaker_id}>"
