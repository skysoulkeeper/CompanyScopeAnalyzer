# modules/directory_initializer.py
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def initialize_directories(reports_directory: str) -> None:
    """
    Initializes necessary directories for the application.

    Args:
        reports_directory (str): Path to the reports directory.
    """
    try:
        reports_path = Path(reports_directory)
        if not reports_path.exists():
            reports_path.mkdir(parents=True)
            logger.info(f"Created reports directory: {reports_path}")
        else:
            logger.info(f"Reports directory already exists: {reports_path}")
    except Exception as e:
        logger.error(f"Error while initializing directories: {e}")
        raise
