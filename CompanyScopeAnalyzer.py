# CompanyScopeAnalyzer.py
from pathlib import Path
import logging
import time
from modules.logger import setup_logging
from modules.config_loader import ConfigLoader
from modules.company_domain_validator import CompanyNameDomainVerifier

def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    verifier = None
    start_time = time.time()  # Start timing the execution
    try:
        config_loader = ConfigLoader(Path('configs/config.yml'))
        config = config_loader.load_config()
        verifier = CompanyNameDomainVerifier(config)
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

