from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, field
from src.domain.models.common.v_enums import LanguageEnum


@dataclass
class TextProcessingConfig:
    # Text cleaning parameters
    remove_extra_whitespace: bool = True
    normalize_unicode: bool = True
    remove_control_chars: bool = True
    preserve_line_breaks: bool = False
    
    # Encoding settings
    default_encoding: str = "utf-8"


@dataclass
class TokenizationConfig:
    # Basic tokenization
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
    # Pattern matching
    use_active_patterns_only: bool = True
    pattern_priority_order: List[str] = field(default_factory=lambda: ["period_specific", "institution_specific", "country_specific"])
    
    # Speaker metadata extraction
    extract_party_info: bool = True
    extract_role_info: bool = True
    normalize_speaker_names: bool = False


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
class RepositoryConfig:
    """Configuration for repository integration."""
    # RegexPattern repository settings
    cache_regex_patterns: bool = True
    pattern_cache_ttl: int = 3600  # 1 hour in seconds
    
    # Future stopwords repository settings
    cache_stopwords: bool = True
    stopwords_cache_ttl: int = 7200  # 2 hours in seconds
    
    # Batch processing
    batch_size: int = 1000
    max_concurrent_operations: int = 5


@dataclass
class APIConfig:
    BASE_URL: str = "https://search.dip.bundestag.de/api/v1/"
    API_KEY: str = "OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw"
    TIMEOUT: int = 10  
    MAX_RETRIES: int = 3


@dataclass
class DatabaseConfig:
    """Configuration for database integration."""
    database_url: str = "sqlite:///../cicero_dev.db"  # FIXME: Replace with env var or config for prod
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
