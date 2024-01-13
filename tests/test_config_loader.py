import unittest
import yaml
import os
from pathlib import Path
from utils.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.valid_config_file = Path('valid_config.yml')
        self.invalid_config_file = Path('invalid_config.yml')
        self.missing_config_file = Path('missing_config.yml')

        with self.valid_config_file.open('w') as file:
            yaml.dump({'key': 'value'}, file)

    def tearDown(self):
        if self.valid_config_file.exists():
            os.remove(self.valid_config_file)
        if self.invalid_config_file.exists():
            os.remove(self.invalid_config_file)

    def test_load_valid_config(self):
        loader = ConfigLoader(self.valid_config_file)
        config = loader.load_config()
        self.assertEqual(config['key'], 'value')

    def test_missing_config_file(self):
        loader = ConfigLoader(self.missing_config_file)
        with self.assertRaises(FileNotFoundError):
            loader.load_config()

    def test_invalid_config_format(self):
        with self.invalid_config_file.open('w') as file:
            file.write('invalid yaml format')
        loader = ConfigLoader(self.invalid_config_file)
        with self.assertRaises(yaml.YAMLError):
            loader.load_config()


if __name__ == '__main__':
    unittest.main()
