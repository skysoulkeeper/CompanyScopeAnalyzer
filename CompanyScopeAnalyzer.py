# CompanyScopeAnalyzer.py
import unittest
from pathlib import Path
import time
import argparse
from utils.logger import setup_logger, logger
from utils.config_loader import ConfigLoader
from utils.directory_initializer import initialize_directories
from modules.company_verification_processor import CompanyProfileValidator


def parse_args():
    parser = argparse.ArgumentParser(description="Company Scope Analyzer")
    parser.add_argument('--config', type=str, default='configs/config.yml',
                        help='Path to the configuration file')
    parser.add_argument('--input', type=str, default='data/input/company.txt',
                        help='Path to the input file with company data')
    parser.add_argument('--report-format', type=str,
                        choices=['csv', 'xml', 'json', 'xls'], default='xls',
                        help='Report format')
    parser.add_argument('--output', type=str, default='data/reports',
                        help='Path to the directory for saving reports')
    parser.add_argument('--report-name', type=str, default='report',
                        help='Report file name')
    parser.add_argument('--log-level', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                        help='Logging level')
    parser.add_argument('--log-file', type=str, help='Path to the log file')
    parser.add_argument('--company-limit', type=int,
                        help='Limit on the number of companies to process')
    parser.add_argument('--domain-limit', type=int,
                        help='Limit on the number of domains to check')
    parser.add_argument('--check-domains', action='store_true',
                        help='Enable domain checking')
    parser.add_argument('--check-companies', action='store_true',
                        help='Enable company checking')
    parser.add_argument('--unit', nargs='?', const='all', default=all,
                        help='Run unit tests. Use --unit all to run all tests')
    return parser.parse_args()


def main() -> None:
    verifier = None
    start_time = time.time()  # Start timing the execution
    args = parse_args()
    if args.unit == 'all':
        loader = unittest.TestLoader()
        start_dir = 'tests'
        suite = loader.discover(start_dir)

        runner = unittest.TextTestRunner()
        runner.run(suite)
        return

    config_path = Path(args.config if args.config else 'configs/config.yml')
    config_loader = ConfigLoader(config_path)
    config = config_loader.load_config()
    setup_logger(config.get('logging', {}))
    try:
        directories_to_create = [
            config.get('input_directory'),
            config.get('reports_directory'),
            config.get('logs_directory')
        ]
        initialize_directories(directories_to_create)
        verifier = CompanyProfileValidator(config)
        verifier.run()  # Run the verifier process
    except Exception as e:
        logger.exception(f"Error occurred during execution: {e}")
    finally:
        if verifier:
            verifier.close()  # Close the verifier resources only if it's initialized
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        logger.info(f"Total execution time: {formatted_time}")


if __name__ == "__main__":
    main()
