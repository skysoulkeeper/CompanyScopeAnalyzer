# modules/company_verification_processor.py
import logging
from pathlib import Path
from datetime import datetime
from .webdriver_setup import setup_webdriver
from modules.reporting.report_generator import ReportGenerator
from .company_name_formatter import format_company_name_to_domain, format_company_name_for_portal
from .portal_factory import get_portal_class
from utils.logger import setup_logging
from .namecheap_domain_checker import DomainAvailabilityChecker

from configs.constants import (
    DEFAULT_STATE_PORTAL_ABBR,
    DEFAULT_COMPANY_NAME_CHECK_ENABLED,
    DEFAULT_DOMAIN_CHECK_ENABLED,
    DEFAULT_DOMAIN_CHECK_LIMIT,
    DEFAULT_COMPANY_CHECK_LIMIT,
    DEFAULT_INPUT_DIRECTORY,
    DEFAULT_REPORTS_DIRECTORY,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_REPORT_FILENAME
)

setup_logging()
logger = logging.getLogger(__name__)


class CompanyProfileValidator:
    def __init__(self, config):
        self.config = config
        self.state_portal_abbr = self.config.get('state_portal_abbr', DEFAULT_STATE_PORTAL_ABBR)
        self.company_name_check_enabled = self.config.get('company_name_check_enabled', DEFAULT_COMPANY_NAME_CHECK_ENABLED)
        self.domain_check_enabled = self.config.get('domain_check_enabled', DEFAULT_DOMAIN_CHECK_ENABLED)
        self.namecheap_search_url = self.config.get('namecheap_search_url')
        self.domain_search_limit = self.config.get('domain_check_limit', DEFAULT_DOMAIN_CHECK_LIMIT)
        self.company_check_limit = self.config.get('company_check_limit', DEFAULT_COMPANY_CHECK_LIMIT)
        self.domain_zones = self.config['domain_zones'][:self.domain_search_limit]
        self.input_directory = self.config.get('input_directory', DEFAULT_INPUT_DIRECTORY)
        self.reports_directory = self.config.get('reports_directory', DEFAULT_REPORTS_DIRECTORY)
        self.report_filename = Path(
            self.reports_directory) / f"{self.config.get('report_filename', DEFAULT_REPORT_FILENAME)}_{datetime.now().strftime('%d_%m_%Y')}"
        self.output_format = self.config.get('output_format', DEFAULT_OUTPUT_FORMAT)

        self.driver = setup_webdriver(config)
        self.results = []
        self.domain_checker = DomainAvailabilityChecker(self.driver, self.namecheap_search_url)

    def run(self):
        company_file_path = Path(self.input_directory) / 'company.txt'
        portal_class = get_portal_class(self.state_portal_abbr)
        portal = portal_class(self.driver)

        try:
            with open(company_file_path, 'r') as file:
                companies = file.readlines()[:self.company_check_limit]
            lines_count = len(companies)
            logger.info("Number of lines in the company file: %s", lines_count)

            for company in companies:
                company_name = company.strip()
                logger.info("Starting processing for company: %s", company_name)

                formatted_name = format_company_name_to_domain(company_name)
                portal_formatted_name = format_company_name_for_portal(company_name)
                result_lines = [f"Company: {company_name}"]

                if self.company_name_check_enabled:
                    bns_status = portal.check_availability(portal_formatted_name)
                    result_lines.append(f"BNS Status: {bns_status}")

                if self.domain_check_enabled:
                    for domain_extension in self.domain_zones:
                        full_domain = formatted_name + domain_extension
                        domain_status = self.domain_checker.check_domain_status(full_domain)
                        result_lines.append(f"{full_domain}: {domain_status}")

                self.results.append(result_lines)
                logger.info("Finished processing for company: %s", company_name)

            self.save_report()
        except FileNotFoundError:
            logger.error(f"File {company_file_path} not found.")
        except Exception as e:
            logger.error("Unexpected error during processing: %s", e)
            logger.exception("Detailed exception information:")
        finally:
            self.close()

    def save_report(self):
        report_generator = ReportGenerator(self.config, self.results)
        report_generator.generate_report()

    def close(self):
        try:
            self.driver.quit()
            logger.info("Web driver closed successfully.")
        except Exception as e:
            logger.error(f"Error closing web driver: {e}")
