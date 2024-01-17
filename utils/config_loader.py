# utils/config_loader.py
from typing import Dict
from pathlib import Path
import yaml
from utils.logger import logger


class ConfigLoader:
    def __init__(self, config_path: Path):
        # Initializes the ConfigLoader with the path to the configuration file.
        self.config_path = config_path

    def load_config(self) -> Dict[str, any]:
        # Loads and returns the configuration from the YAML file.
        # If the file is not found or an error occurs in reading, it logs an error and raises an exception.
        try:
            with open(self.config_path, 'r') as file:
                # Load the YAML configuration file safely.
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError as e:
            # Log an error if the file is not found and re-raise the exception.
            logger.error(f"Configuration file not found: {e}")
            raise
        except yaml.YAMLError as e:
            # Log an error if there is an issue with reading or parsing the YAML file and re-raise the exception.
            logger.error(f"Error reading YAML file: {e}")
            raise
