# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: utils/argument_parser.py

Description:
This module defines the ArgumentParser class, which handles the parsing of command-line
arguments for the Company Scope Analyzer. It supports various options such as configuration
paths, report formats, logging levels, and feature toggles for domain and company checks.
"""

import argparse
from pathlib import Path
from utils.logger import logger


class ArgumentParser:
    def __init__(self):
        # Initializes the argument parser with a description.
        self.parser = argparse.ArgumentParser(description="Company Scope Analyzer")
        self._add_arguments()

    def _add_arguments(self):
        # Defines all command-line arguments the script will accept.
        # --config: Path to the configuration file.
        self.parser.add_argument('--config', type=self._valid_path,
                                 default='configs/config.yml',
                                 help='Path to the configuration file')
        # --input: Path to the input file with company data.
        self.parser.add_argument('--input', type=self._valid_path,
                                 default='data/input/company.txt',
                                 help='Path to the input file with company data')
        # --report-format: The format for reports (csv, xml, json, xls).
        self.parser.add_argument('--report-format', type=str,
                                 choices=['csv', 'xml', 'json', 'xls'], default='xls',
                                 help='Report format')
        # --output: Path to the directory for saving reports.
        self.parser.add_argument('--output', type=self._valid_path,
                                 default='data/reports',
                                 help='Path to the directory for saving reports')
        # --report-name: The file name for the report.
        self.parser.add_argument('--report-name', type=str, default='report',
                                 help='Report file name')
        # --log-level: Logging level (DEBUG, INFO, WARNING, ERROR).
        self.parser.add_argument('--log-level', type=str,
                                 choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                                 default='INFO',
                                 help='Logging level')
        # --log-file: Path to the log file.
        self.parser.add_argument('--log-file', type=self._valid_path,
                                 help='Path to the log file')
        # --company-limit: Limit on the number of companies to process.
        self.parser.add_argument('--company-limit', type=self._positive_int,
                                 help='Limit on the number of companies to process')
        # --domain-limit: Limit on the number of domains to check.
        self.parser.add_argument('--domain-limit', type=self._positive_int,
                                 help='Limit on the number of domains to check')
        # --check-domains: Flag to enable domain checking.
        self.parser.add_argument('--check-domains', action='store_true',
                                 help='Enable domain checking')
        # --check-companies: Flag to enable company checking.
        self.parser.add_argument('--check-companies', action='store_true',
                                 help='Enable company checking')
        # --unit: Option to run unit tests. 'all' runs all tests.
        self.parser.add_argument('--unit', nargs='?', const='all', default=all,
                                 help='Run unit tests. Use --unit all to run all tests')

    def parse_args(self):
        # Parses the command-line arguments and returns them. Logs and raises an error if parsing fails.
        try:
            args = self.parser.parse_args()
            return args
        except SystemExit as e:
            logger.error(f"Error parsing arguments: {e}")
            raise

    @staticmethod
    def _valid_path(path_str):
        # Validates if the provided path string is a valid path.
        if not path_str:
            return None
        path = Path(path_str)
        if not path.exists():
            raise argparse.ArgumentTypeError(f"The path {path_str} does not exist.")
        return path

    @staticmethod
    def _positive_int(value):
        # Validates if the provided value is a positive integer.
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return ivalue
