"""
Configuration management for the Cicero application.
Centralized configuration for all data manipulation parameters.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, field
from src.domain.models.v_enums import LanguageEnum, CountryEnum


@dataclass
class TextProcessingConfig:
    """Configuration for text processing operations."""
    # Language-specific settings
    default_language: LanguageEnum = LanguageEnum.DE
    language_detection_threshold: float = 0.8
    
    # Text cleaning parameters
    remove_extra_whitespace: bool = True
    normalize_unicode: bool = True
    remove_control_chars: bool = True
    preserve_line_breaks: bool = False
    
    # Encoding settings
    default_encoding: str = "utf-8"
    fallback_encodings: List[str] = field(default_factory=lambda: ["latin-1", "cp1252"])


@dataclass
class TokenizationConfig:
    """Configuration for tokenization operations."""
    # Basic tokenization
    lowercase_tokens: bool = True
    remove_punctuation: bool = False
    min_token_length: int = 1
    max_token_length: int = 100
    
    # Language-specific tokenization
    language_specific_rules: Dict[LanguageEnum, Dict[str, Any]] = field(default_factory=dict)
    
    # N-gram settings
    ngram_range: tuple = (1, 3)
    min_ngram_freq: int = 1


@dataclass
class SpeakerExtractionConfig:
    """Configuration for speaker extraction operations."""
    # Pattern matching
    use_active_patterns_only: bool = True
    pattern_priority_order: List[str] = field(default_factory=lambda: ["period_specific", "institution_specific", "country_specific"])
    
    # Speaker metadata extraction
    extract_party_info: bool = True
    extract_role_info: bool = True
    normalize_speaker_names: bool = True
    
    # Fallback settings
    use_fallback_patterns: bool = True
    max_extraction_attempts: int = 3


@dataclass
class CountingConfig:
    """Configuration for text counting operations."""
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
    """Configuration for logging and progress reporting."""
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
class DataManipulationConfig:
    """Main configuration class for all data manipulation operations."""
    text_processing: TextProcessingConfig = field(default_factory=TextProcessingConfig)
    tokenization: TokenizationConfig = field(default_factory=TokenizationConfig)
    speaker_extraction: SpeakerExtractionConfig = field(default_factory=SpeakerExtractionConfig)
    counting: CountingConfig = field(default_factory=CountingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    repository: RepositoryConfig = field(default_factory=RepositoryConfig)
    
    # Global settings
    enable_language_detection: bool = True
    enable_performance_monitoring: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'DataManipulationConfig':
        """Create configuration from dictionary."""
        # Implementation for loading from file/environment
        return cls()
    
    @classmethod
    def default(cls) -> 'DataManipulationConfig':
        """Get default configuration."""
        return cls()
    
    def get_language_config(self, language: LanguageEnum) -> Dict[str, Any]:
        """Get language-specific configuration."""
        base_config = {
            LanguageEnum.DE: {
                "sentence_splitting": True,
                "compound_splitting": False,
                "case_sensitive": False
            },
            LanguageEnum.FR: {
                "sentence_splitting": True,
                "compound_splitting": False,
                "case_sensitive": False
            }
        }
        return base_config.get(language, {})


# Global configuration instance
_config_instance: Optional[DataManipulationConfig] = None


def get_config() -> DataManipulationConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = DataManipulationConfig.default()
    return _config_instance


def set_config(config: DataManipulationConfig) -> None:
    """Set the global configuration instance."""
    global _config_instance
    _config_instance = config