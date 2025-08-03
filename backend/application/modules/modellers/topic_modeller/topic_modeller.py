from typing import List, Dict, Any
from backend.domain.irepository.common.i_corpora import ICorporaRepository
from backend.domain.irepository.text.i_text_clean import ICleanTextRepository
from backend.domain.irepository.text.i_speech_metrics import ISpeechMetricsRepository
from backend.domain.models.common.a_corpora import Corpora
from backend.domain.models.common.v_common import UUID
from backend.domain.models.text.e_speech_metrics_plugin import MetricsPlugin
from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec
from backend.domain.services.modelling.topic_modeller_bert import TopicModeler # FIXME: BRUH

import logging
logger = logging.getLogger(__name__)

class TopicModeller:
    def __init__(
        self,
        corpora_repo: ICorporaRepository,
        clean_text_repo: ICleanTextRepository,
        speech_metrics_repo: ISpeechMetricsRepository,
        topic_modeler: TopicModeler,
    ):
        self.corpora_repo = corpora_repo
        self.clean_text_repo = clean_text_repo
        self.speech_metrics_repo = speech_metrics_repo
        self.topic_modeler = topic_modeler

    # TODO: Needs refactoring, probably should return only model details. Annotation should be down the line and not attempted here
    def build_model(self, spec: TopicModellerSpec) -> Dict[str, Any]:
        corpora: Corpora = spec.corpora
        text_ids = corpora.texts
        texts: List[str] = []
        id_map: Dict[Any, str] = {}
        for tid in text_ids:
            raw = self.clean_text_repo.get_by_speech_id(tid)
            if raw:
                texts.append(raw.text)
                id_map[tid] = raw.text
        if not texts:
            raise ValueError("No texts found for topic modeling.")
        topics, probs = self.topic_modeler.fit(texts)

        logger.info(f"Fitted topic model with {len(topics)} topics.")
        return {
            "topics": topics,
            "probs": probs,
        }

    def annotate_corpora(self, corpora: Corpora) -> Corpora:
        # Extract text IDs from corpora
        text_ids = corpora.texts

        # Build id_to_text mapping for annotation
        id_to_text: Dict[UUID, str] = {}
        for tid in text_ids:
            raw = self.clean_text_repo.get_by_speech_id(tid)
            if raw:
                id_to_text[tid] = raw.text

        if not id_to_text:
            raise ValueError("No texts found for annotation.")

        # Get topic annotations with probabilities (top 3 topics per document)
        logger.info("Annotating topics for corpora.")
        topic_annotations = self.topic_modeler.annotate(id_to_text, top_n=3, include_probs=True)

        # Process annotations and save to speech metrics
        for speech_id, topic_data in topic_annotations.items():
            # Convert topic assignments to dominant_topics format
            dominant_topics: List[Dict[str, float]] = []
            if isinstance(topic_data, list):
                for topic_id, prob in topic_data:
                    dominant_topics.append({"topic_id": float(topic_id), "probability": float(prob)})

            # Get existing metrics or create new ones
            existing_metrics = self.speech_metrics_repo.get_by_speech_id(speech_id)

            if existing_metrics:
                # Update existing metrics with topic data
                existing_metrics.set_dominant_topics(dominant_topics)
                self.speech_metrics_repo.update(speech_id, existing_metrics)
            else:
                # Create new metrics plugin with topic data
                new_metrics = MetricsPlugin(id=UUID.new(), dominant_topics=dominant_topics)
                self.speech_metrics_repo.add(speech_id, new_metrics)

        # Update the corpora in the repository to reflect the annotation
        self.corpora_repo.update(corpora)

        return corpora

    def build_model_and_annotate(self, spec: TopicModellerSpec) -> Dict[str, Any]:
        model_result = self.build_model(spec)
        annotated_corpora = self.annotate_corpora(spec.corpora)

        return {
            **model_result,
            "annotated_corpora": annotated_corpora,
        }
