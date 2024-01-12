# modules/reporting/report_generator.py
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from modules.reporting.xls_writer import XLSReportGenerator
from modules.reporting.xml_writer import XMLReportGenerator
from modules.reporting.json_writer import JSONReportGenerator
from utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, config_params: Dict[str, any], results_list: List[List[str]]):
        self.config_data = config_params
        self.result_data = results_list
        self.report_filename = Path(self.config_data.get('reports_directory',
                                                         'reports')) / f"{self.config_data.get('report_filename', 'result')}_{datetime.now().strftime('%d_%m_%Y')}"

    def generate_report(self) -> None:
        report_format = self.config_data.get('output_format', 'txt').lower()
        logger.info(f"Generating report in {report_format} format.")

        report_methods = {
            'xls': self._generate_xls_report,
            'xml': self._generate_xml_report,
            'json': self._generate_json_report,
            'txt': self._generate_txt_report
        }

        generate_method = report_methods.get(report_format, self._generate_txt_report)
        try:
            generate_method()
        except Exception as e:
            logger.error(f"Error generating {report_format.upper()} report: {e}")
            raise

    def _generate_xls_report(self):
        try:
            logger.info("Generating XLS report.")
            report_generator = XLSReportGenerator(self.config_data['domain_zones'])
            report_generator.write_report(str(self.report_filename), self.result_data)
        except Exception as e:
            logger.error(f"Error generating XLS report: {e}")
            raise

    def _generate_xml_report(self):
        try:
            logger.info("Generating XML report.")
            xml_writer = XMLReportGenerator(str(self.report_filename))
            xml_writer.write_to_xml(self.result_data)
        except Exception as e:
            logger.error(f"Error generating XML report: {e}")
            raise

    def _generate_json_report(self):
        try:
            logger.info("Generating JSON report.")
            json_generator = JSONReportGenerator()
            for result_lines in self.result_data:
                data_dict = {
                    "Company Name": result_lines[0].replace('Company: ', ''),
                    "BNS Status": result_lines[1].split(': ')[1],
                    "Domains": {domain.split(': ')[0]: domain.split(': ')[1] for domain in result_lines[2:]}
                }
                for domain_info in result_lines[2:]:
                    domain, status = domain_info.split(': ')
                    data_dict["Domains"][domain] = status
                json_generator.add_data(data_dict)
            json_generator.save_json(self.report_filename.with_suffix('.json'))
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            raise

    def _generate_txt_report(self):
        try:
            logger.info("Generating TXT report.")
            txt_filename = f"{str(self.report_filename)}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as file:
                for result_lines in self.result_data:
                    for line in result_lines:
                        file.write(line + "\n")
                    file.write(
                        "\n")
        except Exception as e:
            logger.error(f"Error generating TXT report: {e}")
            raise


# Example usage
if __name__ == "__main__":
    config_data = {}
    result_data = []
    report_gen = ReportGenerator(config_data, result_data)
    report_gen.generate_report()
