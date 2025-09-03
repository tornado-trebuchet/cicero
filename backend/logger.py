from typing import Optional
import os
from backend.config import LoggingConfig

from aiologger import Logger as AsyncLogger  # type: ignore[import-not-found]
from aiologger.handlers.streams import AsyncStreamHandler  # type: ignore[import-not-found]
from aiologger.handlers.files import AsyncFileHandler  # type: ignore[import-not-found]
from aiologger.formatters.base import Formatter as AFormatter  # type: ignore

# Minimal level name to numeric value mapping (mirrors stdlib constants)
LEVELS = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


def _level(value: str, fallback: int) -> int:
    if not value:
        return fallback
    return LEVELS.get(value.upper(), fallback)


def setup_logging(config: LoggingConfig) -> Optional[AsyncLogger]:

    level = _level(config.default_log_level, LEVELS["INFO"])
    # aiologger expects a LogLevel enum; passing int works at runtime. Suppress type checker warning.
    async_logger = AsyncLogger(name="root", level=level) # type: ignore[arg-type] 

    # Console handler
    stream_level = _level(config.console_log_level, LEVELS["INFO"])
    fmt = AFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    stream_handler = AsyncStreamHandler(level=stream_level, formatter=fmt)
    async_logger.add_handler(stream_handler)

    # File handler (no rotation handled here)
    if config.log_file_path:
        parent = os.path.dirname(config.log_file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        file_handler = AsyncFileHandler(config.log_file_path)
        file_handler.level = _level(config.file_log_level, LEVELS["DEBUG"])
        file_handler.formatter = fmt
        async_logger.add_handler(file_handler)

    return async_logger


async def shutdown_logger(async_logger: Optional[AsyncLogger]) -> None:
    """Gracefully shutdown an AsyncLogger (await this on application stop)."""
    if not async_logger:
        return
    try:
        await async_logger.shutdown()
    except Exception:
        pass