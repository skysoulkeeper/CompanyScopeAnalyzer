# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: app.py

Description:
This module serves as the main entry point for analyzing company profiles. It handles
configuration loading, directory initialization, and running company profile verification.
It also supports running unit tests if specified by the user.
"""

import time
from pathlib import Path
from utils.logger import setup_logger, logger
from utils.argument_parser import ArgumentParser
from tests.run_tests import run_tests
from utils.config_loader import ConfigLoader
from utils.directory_initializer import initialize_directories
from modules.company_verification_processor import CompanyProfileValidator


# Define the main function
def main() -> None:
    verifier = None
    start_time = time.time()  # Start timing the execution
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()

    # Check if the user specified 'all' as the unit to run tests
    if args.unit == 'all':
        run_tests()
        return

    # Load configuration from a YAML file
    config_path = Path(args.config if args.config else 'configs/config.yml')
    config_loader = ConfigLoader(config_path)
    config = config_loader.load_config()

    # Setup logger based on the configuration settings
    setup_logger(config.get('logging', {}))

    try:
        # Define a list of directories to create based on configuration
        directories_to_create = [
            config.get('input_directory'),
            config.get('reports_directory'),
            config.get('logs_directory')
        ]

        # Initialize necessary directories
        initialize_directories(directories_to_create)

        # Create an instance of the CompanyProfileValidator with the loaded configuration
        verifier = CompanyProfileValidator(config)

        # Run the verification process using the CompanyProfileValidator instance
        verifier.run()

    except Exception as e:
        # Handle exceptions and log any errors that occur during execution
        logger.exception(f"Error occurred during execution: {e}")
    finally:
        if verifier:
            verifier.close()  # Close the verifier resources only if it's initialized
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        logger.info(f"Total execution time: {formatted_time}")


# Entry point of the script
if __name__ == "__main__":
    main()
