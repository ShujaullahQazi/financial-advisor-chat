"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional

from ..config.settings import settings


def setup_logger(name: str = "finai", level: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger instance.

    Args:
        name: Logger name
        level: Log level (defaults to settings.log_level)

    Returns:
        Configured logger instance
    """
    log_level = level or settings.log_level

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid duplicate handlers
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()
