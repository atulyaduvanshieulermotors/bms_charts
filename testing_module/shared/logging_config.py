"""
This module will set basic configuration for loggers.
"""

import logging
from typing import Any

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s - LogGenerationFile: %(module)s - Line Number: %(lineno)d - Log:%(message)s"
)


def setup_logger(name: str, log_file: str, level: Any = logging.INFO) -> Any:
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode="a")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
