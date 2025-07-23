from dataclasses import dataclass

from src.domain.models.common.a_corpora import Corpora


@dataclass
class TopicModellerSpec:
    corpora: Corpora
