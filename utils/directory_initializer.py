# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: utils/directory_initializer.py

Description:
This module provides a function to initialize directories needed for the application.
It creates directories from a provided list, logs the creation process, and handles
any errors that occur during directory initialization.
"""

from utils.logger import logger
from pathlib import Path
from typing import List

def initialize_directories(directories: List[str]) -> None:
    """
    Initializes necessary directories for the application.
    This function attempts to create each directory in the provided list. If the directory
    already exists, it logs that information. If any error occurs during the directory
    creation, it logs an error and re-raises the exception.

    Args:
        directories (List[str]): List of paths to directories that need to be created.
    """
    for directory in directories:
        try:
            directory_path = Path(directory)
            # Create the directory if it does not exist, also create any parent directories if necessary.
            if not directory_path.exists():
                directory_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory_path}")
            else:
                # Log if the directory already exists.
                logger.info(f"Directory already exists: {directory_path}")
        except Exception as e:
            # Log any exceptions that occur during directory creation and re-raise them.
            logger.error(f"Error while initializing directory '{directory}': {e}")
            raise
