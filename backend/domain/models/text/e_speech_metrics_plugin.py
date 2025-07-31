from typing import Any, Optional

from backend.domain.models.base_entity import Entity
from backend.domain.models.common.v_common import UUID


class MetricsPlugin(Entity):
    """
    Very proud Value object that mutates on demand for speech metrics, validated.
    Fields:
        - dominant_topics: List[dict[str, float]]
        - sentiment: dict[str, float]
        - dynamic_codes: List[Any]
    """

    def __init__(
        self,
        id: UUID,
        dominant_topics: Optional[list[dict[str, float]]] = None,
        sentiment: Optional[dict[str, float]] = None,
        dynamic_codes: Optional[list[Any]] = None,
    ):
        super().__init__(id)
        self._dominant_topics = dominant_topics
        self._sentiment = sentiment
        self._dynamic_codes = dynamic_codes

    @property
    def dominant_topics(self) -> Optional[list[dict[str, float]]]:
        return self._dominant_topics

    @property
    def sentiment(self) -> Optional[dict[str, float]]:
        return self._sentiment

    @property
    def dynamic_codes(self) -> Optional[list[Any]]:
        return self._dynamic_codes

    def set_dominant_topics(self, topics: list[dict[str, float]]) -> None:
        self._dominant_topics = topics

    def add_dominant_topic(self, topic: dict[str, float]) -> None:
        if self._dominant_topics is None:
            self._dominant_topics = []
        self._dominant_topics.append(topic)

    def clear_dominant_topics(self) -> None:
        if self._dominant_topics is not None:
            self._dominant_topics.clear()

    def set_sentiment(self, sentiment: dict[str, float]) -> None:
        self._sentiment = sentiment

    def update_sentiment(self, key: str, value: float) -> None:
        if self._sentiment is None:
            self._sentiment = {}
        self._sentiment[key] = value

    def remove_sentiment(self, key: str) -> None:
        if self._sentiment is not None and key in self._sentiment:
            del self._sentiment[key]

    def clear_sentiment(self) -> None:
        if self._sentiment is not None:
            self._sentiment.clear()

    def set_dynamic_codes(self, codes: list[Any]) -> None:
        self._dynamic_codes = codes

    def add_dynamic_code(self, code: Any) -> None:
        if self._dynamic_codes is None:
            self._dynamic_codes = []
        self._dynamic_codes.append(code)

    def clear_dynamic_codes(self) -> None:
        if self._dynamic_codes is not None:
            self._dynamic_codes.clear()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, MetricsPlugin)
            and self._dominant_topics == other._dominant_topics
            and self._sentiment == other._sentiment
            and self._dynamic_codes == other._dynamic_codes
        )

    def __repr__(self) -> str:
        return f"<MetricsPlugin topics={self._dominant_topics} sentiment={self._sentiment}>"
