from typing import List
import logging
from logging.handlers import RotatingFileHandler
from src.config import LoggingConfig

def setup_logging(config: LoggingConfig):
    handlers: List[logging.Handler] = []
    if config.log_file_path:
        file_handler = RotatingFileHandler(
            config.log_file_path,
            maxBytes=config.max_log_file_size,
            backupCount=config.log_file_backup_count
        )
        file_handler.setLevel(getattr(logging, config.file_log_level.upper(), logging.DEBUG))
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        ))
        handlers.append(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.console_log_level.upper(), logging.INFO))
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    ))
    handlers.append(console_handler)

    logging.basicConfig(
        level=getattr(logging, config.default_log_level.upper(), logging.INFO),
        handlers=handlers
    )

    # Suppress DEBUG logs
    logging.getLogger("numba").setLevel(logging.WARNING)
    logging.getLogger("numba.core.byteflow").setLevel(logging.WARNING)