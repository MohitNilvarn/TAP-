# File: app/core/logger.py
import logging
import sys

# Standard Industry Format: Time | Level | Module:Line | Message
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging():
    """
    Configures the root logger. 
    Call this ONCE in main.py at startup.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout) # Print to terminal
        ]
    )

def get_logger(name: str):
    """
    Returns a configured logger instance with a specific name.
    Example: get_logger("TAP.Auth")
    """
    return logging.getLogger(name)