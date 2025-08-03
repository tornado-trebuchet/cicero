import os
from dataclasses import dataclass
from typing import Tuple, List, Optional
from dotenv import load_dotenv

from backend.domain.models.common.v_enums import PipelineType, PipelineStep
load_dotenv()

# --------------------- Text Service Configurations ---------------------

@dataclass
class TextProcessingConfig:
    remove_extra_whitespace: bool = True
    normalize_unicode: bool = True
    remove_control_chars: bool = True
    preserve_line_breaks: bool = False
    default_encoding: str = "utf-8"

@dataclass
class TokenizationConfig:
    lowercase_tokens: bool = True
    remove_punctuation: bool = True
    min_token_length: int = 1
    max_token_length: int = 100
    # TODO: language-specific tokenization settings

    # N-gram settings
    ngram_range: Tuple[int, int] = (1, 3)
    min_ngram_freq: int = 1


@dataclass
class SpeakerExtractionConfig:
    pass


@dataclass
class CountingConfig:
    # Word counting methods
    count_method: str = "whitespace"  # Options: "whitespace", "tokenized", "linguistic"
    exclude_stopwords: bool = False  # Will be used when stopwords are implemented

    # Character counting
    include_whitespace: bool = False
    include_punctuation: bool = True

    # Token counting
    unique_tokens_only: bool = False

# --------------------- Logger Configurations ---------------------

@dataclass
class LoggingConfig:
    log_file_path: str = ".logs/app.log"
    max_log_file_size: int = 5 * 1024 * 1024  # 5 MB
    log_file_backup_count: int = 3
    file_log_level: str = "DEBUG"
    console_log_level: str = "INFO"
    default_log_level: str = "DEBUG"

# --------------------- API Configurations ---------------------

@dataclass
class APIConfig:
    TIMEOUT: int = 10
    MAX_RETRIES: int = 3

# --------------------- Database Configurations ---------------------

@dataclass
class DatabaseConfig:
    """Configuration for database integration."""

    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "")
    database_url: str = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 3600


# --------------------- Topic Modeling Configurations ---------------------


@dataclass
class BERTConfig:
    language: str = "german"
    top_n_words: int = 15
    n_gram_range: Tuple[int, int] = (1, 2)
    min_topic_size: int = 150
    low_memory: bool = True
    calculate_probabilities: bool = False
    verbose: bool = True


@dataclass
class UMAPConfig:
    n_neighbors: int = 150
    min_dist: float = 0.05
    metric: str = "cosine"
    random_state: int = 1640
    n_components: int = 100
    low_memory: bool = True
    n_jobs: int = -1
    verbose: bool = True


@dataclass
class HDBSCANConfig:
    min_cluster_size: int = 250
    min_samples: int = 20
    metric: str = "euclidean"
    cluster_selection_method: str = "leaf"
    cluster_selection_epsilon: float = 0.3
    allow_single_cluster: bool = True
    core_dist_n_jobs: int = -1
    verbose: bool = True


# --------------------- Pipeline Configurations ---------------------

@dataclass
class PipelineConfig:
    """Configuration for pipeline execution"""
    pipeline_type: PipelineType
    steps: Optional[List[PipelineStep]] = None  # For custom pipelines
    parallel_preprocessing: bool = False  # Process speeches in parallel
    batch_size: Optional[int] = None  # Batch size for processing
    continue_on_error: bool = False  # Continue if individual items fail
    save_intermediate_results: bool = True  # Save results after each step
