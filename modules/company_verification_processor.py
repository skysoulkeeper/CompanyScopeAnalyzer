# modules/company_verification_processor.py
from pathlib import Path
from datetime import datetime
from .webdriver_setup import setup_webdriver
from modules.reporting.report_generator import ReportGenerator
from .company_name_formatter import format_company_name_to_domain, format_company_name_for_portal
from .portal_factory import get_portal_class
from utils.logger import logger
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


# Define a class for processing company profile validation
class CompanyProfileValidator:
    def __init__(self, config):
        # Initialize the validator with configuration settings
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

        # Initialize a WebDriver instance using the setup_webdriver function
        self.driver = setup_webdriver(config)
        self.results = []
        self.domain_checker = DomainAvailabilityChecker(self.driver, self.namecheap_search_url)

    def run(self):
        # Define the path to the input file containing company names
        company_file_path = Path(self.input_directory) / 'company.txt'
        portal_class = get_portal_class(self.state_portal_abbr)
        # Get the portal class based on the state abbreviation
        portal = portal_class(self.driver)

        try:
            with open(company_file_path, 'r') as file:
                # Read company names from the file (up to the specified limit)
                companies = file.readlines()[:self.company_check_limit]
            lines_count = len(companies)
            logger.info("The number of companies to be processed from the file is: {}", lines_count)

            for company in companies:
                company_name = company.strip()
                logger.info("Starting processing for company: {}", company_name)

                # Format the company name for domain and portal
                formatted_name = format_company_name_to_domain(company_name)
                portal_formatted_name = format_company_name_for_portal(company_name)
                result_lines = [f"Company: {company_name}"]

                if self.company_name_check_enabled:
                    # Check BNS availability for the formatted company name
                    bns_status = portal.check_availability(portal_formatted_name)
                    result_lines.append(f"BNS status: {bns_status}")

                if self.domain_check_enabled:
                    for domain_extension in self.domain_zones:
                        full_domain = formatted_name + domain_extension
                        # Check domain availability using DomainAvailabilityChecker
                        domain_status = self.domain_checker.check_domain_status(full_domain)
                        result_lines.append(f"{full_domain}: {domain_status}")

                self.results.append(result_lines)
                logger.info("Finished processing for company: {}", company_name)

            # Save the generated report
            self.save_report()
        except FileNotFoundError:
            logger.error(f"File {company_file_path} not found.")
        except Exception as e:
            logger.error("Unexpected error during processing: {}", e)
            logger.exception("Detailed exception information:")
        finally:
            # Close the WebDriver
            self.close()

    def save_report(self):
        # Get the state abbreviation for the report
        state_abbr = self.config.get('state_portal_abbr', 'Unknown')
        # Generate and save the report using ReportGenerator
        report_generator = ReportGenerator(self.config, self.results, state_abbr)
        report_generator.generate_report()

    def close(self):
        try:
            # Quit the WebDriver
            self.driver.quit()
            logger.info("Web driver closed successfully.")
        except Exception as e:
            logger.error(f"Error closing web driver: {e}")
