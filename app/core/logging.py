"""Project-wide logging configuration using loguru.

This module provides centralized logging configuration for the FastAPI
application using the loguru library. It sets up console, file, and error
logging with appropriate formatting and rotation policies.
"""

import sys
from pathlib import Path

from loguru import logger


def setup_logging() -> None:
    """Configure project-wide logging with loguru.

    Sets up three logging handlers:
    1. Console output with colored formatting
    2. Application log file with rotation and compression
    3. Error log file for error-level messages only
    """
    logger.remove()

    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app.log",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} | {message}"
        ),
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        log_dir / "error.log",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} | {message}"
        ),
        level="ERROR",
        rotation="5 MB",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )

    logger.info("Logging configured successfully")


def get_logger(name: str) -> logger:
    """Get a logger instance for a specific module.

    Args:
        name: The name of the module (usually __name__)

    Returns:
        Logger instance bound to the specified module name
    """
    return logger.bind(name=name)


setup_logging()
