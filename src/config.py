import os
from dataclasses import dataclass
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()


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


@dataclass
class LoggingConfig:
    log_file_path: str = "logs/app.log"
    max_log_file_size: int = 5 * 1024 * 1024  # 5 MB
    log_file_backup_count: int = 3
    file_log_level: str = "DEBUG"
    console_log_level: str = "INFO"
    default_log_level: str = "DEBUG"


@dataclass
class APIConfig:
    TIMEOUT: int = 10
    MAX_RETRIES: int = 3


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
