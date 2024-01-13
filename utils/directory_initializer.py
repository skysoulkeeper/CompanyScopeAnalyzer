# utils/directory_initializer.py
from utils.logger import logger
from pathlib import Path
from typing import List



def initialize_directories(directories: List[str]) -> None:
    """
    Initializes necessary directories for the application.

    Args:
        directories (List[str]): List of paths to directories that need to be created.
    """
    for directory in directories:
        try:
            directory_path = Path(directory)
            if not directory_path.exists():
                directory_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory_path}")
            else:
                logger.info(f"Directory already exists: {directory_path}")
        except Exception as e:
            logger.error(f"Error while initializing directory '{directory}': {e}")
            raise
