from dataclasses import dataclass

from backend.domain.models.common.a_corpora import Corpora


@dataclass
class TopicModellerSpec:
    corpora: Corpora
