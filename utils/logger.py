# utils/logger.py
import logging


def setup_logging():
    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
