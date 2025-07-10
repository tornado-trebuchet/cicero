from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
from src.domain.models.common.v_enums import LanguageEnum
from dotenv import load_dotenv
import os

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
    
    # Language-specific tokenization
    language_specific_rules: Dict[LanguageEnum, Dict[str, Any]] = field(default_factory=dict)
    
    # N-gram settings
    ngram_range: tuple = (1, 3)
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
    # Logging levels
    default_log_level: str = "INFO"
    file_log_level: str = "DEBUG"
    console_log_level: str = "INFO"
    
    # Progress reporting
    enable_progress_bars: bool = True
    progress_update_frequency: int = 100  # Update every N items
    
    # Log file settings
    log_file_path: Optional[Path] = None
    max_log_file_size: int = 10 * 1024 * 1024  # 10MB
    log_file_backup_count: int = 5

@dataclass
class APIConfig:
    BASE_URL: str = "https://search.dip.bundestag.de/api/v1/" # We will dynamically sort it out later
    API_KEY: str = os.environ.get("API_KEY", "")
    TIMEOUT: int = 10  
    MAX_RETRIES: int = 3


@dataclass
class DatabaseConfig:
    """Configuration for database integration."""
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT","")
    database_url: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
