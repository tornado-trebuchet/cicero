from typing import List, Dict, Any
from src.domain.irepository.common.i_corpora import ICorporaRepository
from src.domain.irepository.text.i_text_clean import ICleanTextRepository
from src.domain.models.common.a_corpora import Corpora
from src.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec
from src.domain.services.modelling.topic_modeller_bert import TopicModeler

class TopicModeller:
    def __init__(
        self,
        corpora_repo: ICorporaRepository,
        raw_text_repo: ICleanTextRepository,
        topic_modeler: TopicModeler,
    ):
        self.corpora_repo = corpora_repo
        self.raw_text_repo = raw_text_repo
        self.topic_modeler = topic_modeler

    def model_topics(self, spec: TopicModellerSpec) -> Dict[str, Any]:
        corpora: Corpora = spec.corpora
        text_ids = corpora.texts
        texts: List[str] = []
        id_map: Dict[Any, str] = {}
        for tid in text_ids:
            raw = self.raw_text_repo.get_by_speech_id(tid)
            if raw:
                texts.append(raw.text)
                id_map[tid] = raw.text
        if not texts:
            raise ValueError("No texts found for topic modeling.")
        topics, probs = self.topic_modeler.fit(texts)
        return {
            "topics": topics,
            "probs": probs,
            "id_map": id_map
        }

    def annotate_corpora(self, corpora: Corpora) -> Corpora:
        """
        Annotate the corpora with topics and probabilities.
        """
        return corpora