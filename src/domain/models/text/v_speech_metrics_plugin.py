from typing import Any, Optional
from src.domain.models.common.base_model import ValueObject

class MetricsPlugin(ValueObject):
    """
    Very proud Value object that mutates on demand for speech metrics, validated.
    Fields:
        - dominant_topics: List[dict[str, float]]
        - sentiment: dict[str, float]
        - dynamic_codes: List[Any]
    """
    def __init__(self, dominant_topics: Optional[list[dict[str, float]]] = None, sentiment: Optional[dict[str, float]] = None, dynamic_codes: Optional[list[Any]] = None):
        self._dominant_topics = dominant_topics if dominant_topics is not None else []
        self._sentiment = sentiment if sentiment is not None else {}
        self._dynamic_codes = dynamic_codes if dynamic_codes is not None else []

    @property
    def dominant_topics(self):
        return self._dominant_topics

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def dynamic_codes(self):
        return self._dynamic_codes

    def set_dominant_topics(self, topics: list[dict[str, float]]):
        self._dominant_topics = topics

    def add_dominant_topic(self, topic: dict[str, float]):
        self._dominant_topics.append(topic)

    def clear_dominant_topics(self):
        self._dominant_topics.clear()

    def set_sentiment(self, sentiment: dict[str, float]):
        self._sentiment = sentiment

    def update_sentiment(self, key: str, value: float):
        self._sentiment[key] = value

    def remove_sentiment(self, key: str):
        if key in self._sentiment:
            del self._sentiment[key]

    def clear_sentiment(self):
        self._sentiment.clear()

    def set_dynamic_codes(self, codes: list[Any]):
        self._dynamic_codes = codes

    def add_dynamic_code(self, code: Any):
        self._dynamic_codes.append(code)

    def clear_dynamic_codes(self):
        self._dynamic_codes.clear()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MetricsPlugin)
            and self._dominant_topics == other._dominant_topics
            and self._sentiment == other._sentiment
            and self._dynamic_codes == other._dynamic_codes
        )

    def __repr__(self) -> str:
        return f"<MetricsPlugin topics={self._dominant_topics} sentiment={self._sentiment}>"
