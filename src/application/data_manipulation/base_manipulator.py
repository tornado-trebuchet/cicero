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
    language: LanguageEnum
    country: CountryEnum
    institution_id: UUID
    period_id: Optional[UUID] = None
    batch_size: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ProgressInfo:
    current: int
    total: int
    start_time: float
    current_time: float
    
    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.current / self.total) * 100.0
    
    @property
    def elapsed_time(self) -> float:
        return self.current_time - self.start_time
    
    @property
    def estimated_remaining(self) -> Optional[float]:
        if self.current == 0 or self.elapsed_time == 0:
            return None
        rate = self.current / self.elapsed_time
        remaining_items = self.total - self.current
        return remaining_items / rate if rate > 0 else None


class BaseManipulator(ABC, Generic[T, R]):  
    def __init__(self, config: Optional[DataManipulationConfig] = None):
        self._config = config or get_config()
        self._logger = self._setup_logger()
        self._progress_callback: Optional[Callable[[ProgressInfo], None]] = None
    
    def _setup_logger(self) -> logging.Logger:
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
        self._progress_callback = callback
    
    def _report_progress(self, current: int, total: int, start_time: float) -> None:
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
    
    def _validate_input(self, data: T, context: ProcessingContext) -> bool:
        if data is None:
            self._logger.warning("Input data is None")
            return False
        
        # Additional validation can be implemented in subclasses
        return True
    
    def _get_language_config(self, language: LanguageEnum) -> Dict[str, Any]:
        return self._config.get_language_config(language)
    
    @abstractmethod
    def process_single(self, data: T, context: ProcessingContext) -> R:
        pass

    @abstractmethod
    def process_batch(self, items: List[T], context: ProcessingContext) -> List[R]:
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
        context = ProcessingContext(**context_kwargs)
        return self.process_single(data, context)
    
    def process_batch_with_context(self, items: List[T], **context_kwargs) -> List[R]:
        context = ProcessingContext(**context_kwargs)
        return self.process_batch(items, context)
    
    @property
    def config(self) -> DataManipulationConfig:
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        return self._logger