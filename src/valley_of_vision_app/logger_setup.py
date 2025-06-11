import logging
import sys
from pathlib import Path

def setup_logger(log_file_path: Path):
    """
    Configures a centralized logger to output to both console and a file.
    """
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # --- Create File Handler with UTF-8 encoding ---
    # This ensures emojis and other special characters are handled correctly.
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # --- Create Console Handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(message)s') # Keep console output clean
    console_handler.setFormatter(console_formatter)

    # Clear existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add both handlers to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
