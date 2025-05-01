"""Logging configuration for MycoMonitor."""

import logging
import os
from typing import Optional

def setup_logging(
    log_file: Optional[str] = "/var/log/mycomonitor.log",
    level: int = logging.INFO,
) -> None:
    """Configure logging for the application."""
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s %(levelname)s:%(message)s",
    )

    # Add console handler if no file specified
    if not log_file:
        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)
