from dataclasses import asdict
from typing import Any, List, Tuple, Union, Dict, Optional
import numpy as np
import numpy.typing as npt
import pandas as pd
from bertopic import BERTopic  # type: ignore
from umap import UMAP  # type: ignore
from hdbscan import HDBSCAN  # type: ignore
from sentence_transformers import SentenceTransformer

from src.config import (
    SentenceTransformerConfig,
    BERTConfig,
    UMAPConfig,
    HDBSCANConfig,
)

# --------------------- TopicModeler Wrapper ---------------------
class TopicModeler:
    embedding_model: SentenceTransformer
    umap_model: UMAP
    hdbscan_model: HDBSCAN
    model: BERTopic

    def __init__(
        self,
        bert_config: BERTConfig = BERTConfig(),
        st_config: SentenceTransformerConfig = SentenceTransformerConfig(),
        umap_config: UMAPConfig = UMAPConfig(),
        hdbscan_config: HDBSCANConfig = HDBSCANConfig(),
        **kwargs: Any
    ) -> None:
        """
        Initialize the BERTopic pipeline with configurable embeddings, UMAP, and HDBSCAN.
        """
        # Configs
        self.bert_config: BERTConfig = bert_config
        self.st_config: SentenceTransformerConfig = st_config
        self.umap_config: UMAPConfig = umap_config
        self.hdbscan_config: HDBSCANConfig = hdbscan_config

        # Sentence embedding model
        self.embedding_model = SentenceTransformer(st_config.embedding_model, device=st_config.device)

        # UMAP for dimensionality reduction
        umap_params = asdict(umap_config)
        self.umap_model = UMAP(**umap_params)

        # HDBSCAN for clustering
        hdbscan_params = asdict(hdbscan_config)
        self.hdbscan_model = HDBSCAN(**hdbscan_params)

        # BERTopic combines embedding, UMAP, and HDBSCAN
        bert_params = asdict(bert_config)
        self.model = BERTopic(
            embedding_model=self.embedding_model,
            umap_model=self.umap_model,
            hdbscan_model=self.hdbscan_model,
            **bert_params,
            **kwargs
        )

    def fit(self, documents: List[str]) -> Tuple[List[int], npt.NDArray[np.float_]]:
        """
        Fit the BERTopic model on input documents.

        Args:
            documents: List of raw text documents.

        Returns:
            topics: List of integer topic IDs per document.
            probs:   Array of probabilities shape (n_docs, n_topics).
        """
        topics, probs = self.model.fit_transform(documents)  # type: ignore
        return topics, probs  # type: ignore

    def transform(self, new_documents: List[str]) -> Tuple[List[int], npt.NDArray[np.float_]]:
        """
        Infer topics for new, unseen documents.

        Args:
            new_documents: List of raw text documents.

        Returns:
            topics: List of integer topic IDs per new document.
            probs:   Array of probabilities shape (n_new, n_topics).
        """
        topics, probs = self.model.transform(new_documents)  # type: ignore
        return topics, probs  # type: ignore

    def annotate(
        self, id_to_text: Dict[Any, str], top_n: int = 1, include_probs: bool = False
    ) -> Dict[Any, Union[int, List[Tuple[int, float]]]]:
        """
        Assign topics back to document IDs, optionally returning top‑n topics with probabilities.

        Args:
            id_to_text: Mapping of document ID to its text content.
            top_n:      Number of top topics to return per document.
            include_probs: Whether to include probability scores.

        Returns:
            Mapping from document ID to either a single topic ID or list of (topic, prob) tuples.
        """
        texts = list(id_to_text.values())
        docs_ids = list(id_to_text.keys())
        topics, probs = self.transform(texts)
        result: Dict[Any, Union[int, List[Tuple[int, float]]]] = {}
        for idx, doc_id in enumerate(docs_ids):
            if include_probs:
                # get top_n topics by probability
                top_idxs = np.argsort(probs[idx])[::-1][:top_n]
                result[doc_id] = [(int(t), float(probs[idx, t])) for t in top_idxs]
            else:
                result[doc_id] = int(topics[idx])
        return result

    def get_dynamic_topics(
        self, documents: List[str], topics: List[int], time_labels: List[Union[str, pd.Timestamp]]
    ) -> pd.DataFrame:
        """
        Generate a DataFrame tracking topic prevalence over time.

        Args:
            documents:   Original documents list.
            topics:      List of topic IDs per document.
            time_labels: Corresponding time labels (date or string).

        Returns:
            DataFrame with columns ['Topic', 'Timestamp', 'Frequency', ...].
        """
        return self.model.topics_over_time(documents, topics, time_labels)  # type: ignore

    def get_topic_info(self) -> pd.DataFrame:
        """
        Retrieve topic summary including term frequencies and sizes.

        Returns:
            DataFrame with columns ['Topic', 'Name', 'Count', ...].
        """
        return self.model.get_topic_info()

    def save(self, filepath: str) -> None:
        self.model.save(filepath)  # type: ignore

    @classmethod
    def load(
        cls,
        filepath: str,
        bert_config: Optional[BERTConfig] = None,
        st_config: Optional[SentenceTransformerConfig] = None,
        umap_config: Optional[UMAPConfig] = None,
        hdbscan_config: Optional[HDBSCANConfig] = None,
    ) -> "TopicModeler":
        """
        Load a persisted BERTopic model from disk into a TopicModeler instance.
        """
        # Instantiate with provided configs or defaults
        instance = cls(
            bert_config or BERTConfig(),
            st_config or SentenceTransformerConfig(),
            umap_config or UMAPConfig(),
            hdbscan_config or HDBSCANConfig(),
        )
        instance.model = BERTopic.load(filepath)  # type: ignore
        return instance
