from __future__ import annotations

import logging
import os
from pathlib import Path


def setup_logger() -> logging.Logger:
    """
    Configure application-wide logging.

    - Console handler always active.
    - File handlers write to logs/server.log and logs/errors.log
      (directories are created automatically).
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(level=logging.INFO, format=fmt, datefmt=datefmt)

    root_logger = logging.getLogger()

    # Server log (INFO and above)
    file_handler = logging.FileHandler(log_dir / "server.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    root_logger.addHandler(file_handler)

    # Error log (WARNING and above)
    error_handler = logging.FileHandler(log_dir / "errors.log", encoding="utf-8")
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    root_logger.addHandler(error_handler)

    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    return logging.getLogger("chad")