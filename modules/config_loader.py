# modules/config_loader.py
from typing import Dict
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self, config_path: Path):
        self.config_path = config_path

    def load_config(self) -> Dict[str, any]:
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error reading YAML file: {e}")
            raise
