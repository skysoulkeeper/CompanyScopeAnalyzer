# modules/company_domain_validator.py
import logging
from pathlib import Path
from datetime import datetime
from .webdriver_setup import setup_webdriver
from .xls_writer import ExcelReportGenerator
from .xml_writer import XMLWriter
from .company_name_formatter import format_company_name_to_domain, format_company_name_for_portal
from .directory_initializer import initialize_directories
from .portal_factory import get_portal_class
from .logger import setup_logging
from .company_domain_checker import CompanyDomainChecker as DomainChecker

setup_logging()
logger = logging.getLogger(__name__)


class CompanyNameDomainVerifier:
    def __init__(self, config):
        self.config = config
        self.state_portal_abbr = self.config.get('state_portal_abbr', 'NJ')
        self.company_name_check_enabled = self.config.get('company_name_check_enabled', True)
        self.domain_check_enabled = self.config.get('domain_check_enabled', True)
        self.namecheap_search_url = self.config.get('namecheap_search_url')
        self.domain_search_limit = self.config.get('domain_search_limit', 2)
        self.domain_zones = self.config['domain_zones'][:self.domain_search_limit]
        self.input_directory = self.config.get('input_directory', 'data')
        self.reports_directory = self.config.get('reports_directory', 'reports')
        self.report_filename = Path(
            self.reports_directory) / f"{self.config.get('report_filename', 'result')}_{datetime.now().strftime('%d_%m_%Y')}"
        self.output_format = self.config.get('output_format', 'xls')
        self.enable_logging_to_file = self.config.get('enable_logging_to_file', False)

        self.driver = setup_webdriver(config)
        #        self.domain_checker = DomainChecker(self.driver, config['domain_selectors'])
        initialize_directories(self.reports_directory)
        self.results = []
        self.domain_checker = DomainChecker(self.driver, self.namecheap_search_url)

    def run(self):
        company_file_path = Path(self.input_directory) / 'company.txt'
        PortalClass = get_portal_class(self.state_portal_abbr)
        portal = PortalClass(self.driver)

        try:
            with open(company_file_path, 'r') as file:
                companies = file.readlines()
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
        report_filename_str = str(self.report_filename)
        logger.info("Report file saving is starting.")
        if self.output_format.lower() == 'xls':
            report_generator = ExcelReportGenerator(self.domain_zones)
            report_generator.write_report(report_filename_str, self.results)
        elif self.output_format.lower() == 'xml':
            xml_writer = XMLWriter(report_filename_str)
            xml_writer.write_to_xml(self.results)
        elif self.output_format.lower() == 'txt':
            with open(f"{report_filename_str}.txt", 'w', encoding='utf-8') as result_file:
                for result_lines in self.results:
                    for line in result_lines:
                        result_file.write(line + "\n")
            logger.info(f"Generated report file saved: {report_filename_str}.txt")

    def close(self):
        try:
            self.driver.quit()
            logger.info("Web driver closed successfully.")
        except Exception as e:
            logger.error(f"Error closing web driver: {e}")
