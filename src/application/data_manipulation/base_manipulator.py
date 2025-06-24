"""
Base manipulator class providing common functionality for all data manipulation operations.
Includes logging, progress reporting, and configuration management.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Callable
from dataclasses import dataclass
from contextlib import contextmanager

from src.config import get_config, DataManipulationConfig
from src.domain.models.v_enums import LanguageEnum, CountryEnum
from src.domain.models.v_common import UUID


T = TypeVar('T')
R = TypeVar('R')


@dataclass
class ProcessingContext:
    """Context information for data manipulation operations."""
    language: Optional[LanguageEnum] = None
    country: Optional[CountryEnum] = None
    institution_id: Optional[UUID] = None
    period_id: Optional[UUID] = None
    batch_size: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ProgressInfo:
    """Progress information for batch operations."""
    current: int
    total: int
    start_time: float
    current_time: float
    
    @property
    def percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total == 0:
            return 100.0
        return (self.current / self.total) * 100.0
    
    @property
    def elapsed_time(self) -> float:
        """Calculate elapsed time in seconds."""
        return self.current_time - self.start_time
    
    @property
    def estimated_remaining(self) -> Optional[float]:
        """Estimate remaining time in seconds."""
        if self.current == 0 or self.elapsed_time == 0:
            return None
        rate = self.current / self.elapsed_time
        remaining_items = self.total - self.current
        return remaining_items / rate if rate > 0 else None


class BaseManipulator(ABC, Generic[T, R]):
    """
    Abstract base class for all data manipulation operations.
    
    Provides:
    - Logging capabilities
    - Progress reporting for batch operations
    - Configuration management
    - Language-aware processing context
    - Error handling patterns
    """
    
    def __init__(self, config: Optional[DataManipulationConfig] = None):
        """Initialize the manipulator with optional configuration."""
        self._config = config or get_config()
        self._logger = self._setup_logger()
        self._progress_callback: Optional[Callable[[ProgressInfo], None]] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger for this manipulator."""
        logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        logger = logging.getLogger(logger_name)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, self._config.logging.console_log_level))
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # File handler (if configured)
            if self._config.logging.log_file_path:
                from logging.handlers import RotatingFileHandler
                file_handler = RotatingFileHandler(
                    self._config.logging.log_file_path,
                    maxBytes=self._config.logging.max_log_file_size,
                    backupCount=self._config.logging.log_file_backup_count
                )
                file_handler.setLevel(getattr(logging, self._config.logging.file_log_level))
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        
        logger.setLevel(getattr(logging, self._config.logging.default_log_level))
        return logger
    
    def set_progress_callback(self, callback: Callable[[ProgressInfo], None]) -> None:
        """Set callback function for progress updates."""
        self._progress_callback = callback
    
    def _report_progress(self, current: int, total: int, start_time: float) -> None:
        """Report progress if callback is set and conditions are met."""
        if (self._progress_callback and 
            self._config.logging.enable_progress_bars and
            current % self._config.logging.progress_update_frequency == 0):
            
            progress_info = ProgressInfo(
                current=current,
                total=total,
                start_time=start_time,
                current_time=time.time()
            )
            self._progress_callback(progress_info)
    
    @contextmanager
    def _operation_context(self, operation_name: str, context: ProcessingContext):
        """Context manager for operations with logging and error handling."""
        start_time = time.time()
        self._logger.info(f"Starting {operation_name} with context: {context}")
        
        try:
            yield
            elapsed = time.time() - start_time
            self._logger.info(f"Completed {operation_name} in {elapsed:.2f}s")
            
        except Exception as e:
            elapsed = time.time() - start_time
            self._logger.error(f"Failed {operation_name} after {elapsed:.2f}s: {str(e)}")
            raise
    
    def _detect_language(self, text: str, context: ProcessingContext) -> LanguageEnum:
        """
        Detect or determine language for text processing.
        
        Args:
            text: Text to analyze
            context: Processing context with potential language hint
            
        Returns:
            Detected or default language
        """
        # Use context language if provided
        if context.language:
            return context.language
        
        # Simple heuristic-based detection (placeholder for future enhancement)
        if not self._config.enable_language_detection:
            return self._config.text_processing.default_language
        
        # Basic language detection heuristics
        text_lower = text.lower()
        
        # German indicators
        german_indicators = ['der', 'die', 'das', 'und', 'ist', 'eine', 'einen', 'mit', 'von', 'zu']
        # French indicators  
        french_indicators = ['le', 'la', 'les', 'de', 'et', 'est', 'une', 'avec', 'pour', 'sur']
        
        german_score = sum(1 for word in german_indicators if word in text_lower)
        french_score = sum(1 for word in french_indicators if word in text_lower)
        
        if german_score > french_score and german_score > 0:
            detected_language = LanguageEnum.DE
        elif french_score > 0:
            detected_language = LanguageEnum.FR
        else:
            detected_language = self._config.text_processing.default_language
        
        self._logger.debug(f"Language detection: German={german_score}, French={french_score}, Selected={detected_language}")
        return detected_language
    
    def _validate_input(self, data: T, context: ProcessingContext) -> bool:
        """
        Validate input data before processing.
        
        Args:
            data: Input data to validate
            context: Processing context
            
        Returns:
            True if valid, False otherwise
        """
        if data is None:
            self._logger.warning("Input data is None")
            return False
        
        # Additional validation can be implemented in subclasses
        return True
    
    def _get_language_config(self, language: LanguageEnum) -> Dict[str, Any]:
        """Get language-specific configuration."""
        return self._config.get_language_config(language)
    
    @abstractmethod
    def process_single(self, data: T, context: ProcessingContext) -> R:
        """
        Process a single item.
        
        Args:
            data: Single item to process
            context: Processing context
            
        Returns:
            Processed result
        """
        pass
    
    def process_batch(self, items: List[T], context: ProcessingContext) -> List[R]:
        """
        Process a batch of items with progress reporting.
        
        Args:
            items: List of items to process
            context: Processing context
            
        Returns:
            List of processed results
        """
        operation_name = f"batch_process_{len(items)}_items"
        
        with self._operation_context(operation_name, context):
            results = []
            start_time = time.time()
            total_items = len(items)
            
            for i, item in enumerate(items, 1):
                try:
                    if not self._validate_input(item, context):
                        self._logger.warning(f"Skipping invalid item at index {i-1}")
                        continue
                    
                    result = self.process_single(item, context)
                    results.append(result)
                    
                    self._report_progress(i, total_items, start_time)
                    
                except Exception as e:
                    self._logger.error(f"Error processing item at index {i-1}: {str(e)}")
                    metadata = context.metadata or {}
                    if metadata.get('continue_on_error', True):
                        continue
                    else:
                        raise
            
            self._logger.info(f"Successfully processed {len(results)}/{total_items} items")
            return results
    
    def process_single_with_context(self, data: T, **context_kwargs) -> R:
        """
        Convenience method to process single item with context creation.
        
        Args:
            data: Item to process
            **context_kwargs: Context parameters
            
        Returns:
            Processed result
        """
        context = ProcessingContext(**context_kwargs)
        return self.process_single(data, context)
    
    def process_batch_with_context(self, items: List[T], **context_kwargs) -> List[R]:
        """
        Convenience method to process batch with context creation.
        
        Args:
            items: Items to process
            **context_kwargs: Context parameters
            
        Returns:
            List of processed results
        """
        context = ProcessingContext(**context_kwargs)
        return self.process_batch(items, context)
    
    @property
    def config(self) -> DataManipulationConfig:
        """Get current configuration."""
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger instance."""
        return self._logger