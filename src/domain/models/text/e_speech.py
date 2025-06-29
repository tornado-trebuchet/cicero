from typing import Optional
from domain.models.common.v_common import UUID
from domain.models.common.base_model import Entity
from domain.models.text.ve_text import Text
from domain.models.context.ve_speaker import Speaker
from domain.models.text.ve_speech_metrics_plugin import MetricsPlugin
from domain.models.common.ve_metadata_plugin import MetadataPlugin
class Speech(Entity):
    """
    Represents a speech in a protocol, with speaker, text, metrics, and metadata.
    """
    def __init__(
        self,
        id: UUID,
        protocol_id: UUID,
        speaker: Speaker,
        text: Text,
        metadata: Optional[MetadataPlugin] = None,
        metrics: Optional[MetricsPlugin] = None,
    ):
        super().__init__(id)
        self._protocol_id = protocol_id
        self._speaker = speaker
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
    def speaker(self) -> Speaker:
        return self._speaker

    @speaker.setter
    def speaker(self, value: Speaker):
        self._speaker = value

    @property
    def text(self) -> Text:
        return self._text

    @text.setter
    def text(self, value: Text):
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
        return f"<Speech {self.id} by {self._speaker}>"
