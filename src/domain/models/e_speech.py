from typing import Optional, Any
from src.domain.models.v_common import UUID
from src.domain.models.base_model import Entity
from src.domain.models.ve_text import Text
from src.domain.models.ve_speaker import Speaker
from src.domain.models.ve_metrics_plugin import MetricsPlugin
from src.domain.models.ve_metadata_plugin import MetadataPlugin
class Speech(Entity):
    """
    Represents a speech in a protocol, with author, text, metrics, and metadata.
    """
    def __init__(
        self,
        id: UUID,
        protocol_id: UUID,
        author: Speaker,
        text: Text,
        metadata: Optional[MetadataPlugin] = None,
        metrics: Optional[MetricsPlugin] = None,
    ):
        super().__init__(id)
        self._protocol_id = protocol_id
        self._author = author
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
    def author(self) -> Speaker:
        return self._author

    @author.setter
    def author(self, value: Speaker):
        self._author = value

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
        return f"<Speech {self.id} by {self._author}>"
