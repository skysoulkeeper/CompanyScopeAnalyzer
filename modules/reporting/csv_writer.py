# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/reporting/csv_report_generator.py

Description:
This module defines the CSVReportGenerator class, which handles the creation of
CSV reports. It writes headers and data to a CSV file based on the provided results
and supports dynamic data formatting for domain availability checks.
"""

import csv
from typing import List
from pathlib import Path
from utils.logger import logger


# Define a class for generating CSV reports
class CSVReportGenerator:
    def __init__(self, domain_zones: List[str], state: str):
        self.domain_zones = domain_zones
        self.state = state

    def _write_header(self, csv_writer, headers: List[str]):
        try:
            # Write the headers to the CSV file
            csv_writer.writerow(headers)
        except Exception as e:
            logger.error(f"Error while writing CSV header: {e}")
            raise

    def _write_data(self, csv_writer, results: List[List[str]]):
        logger.info("Writing data to CSV")
        try:
            # Iterate through the results and write data to the CSV file
            for result_lines in results:
                company_data = [result_lines[0].replace('Company: ', ''), self.state,
                                result_lines[1].split(': ')[1]]

                for domain_zone in self.domain_zones:
                    for line in result_lines[2:]:
                        if f"{domain_zone}" in line:
                            dynamic_value = line.split(': ')[1]
                            company_data.append(dynamic_value)
                            break

                csv_writer.writerow(company_data)
        except Exception as e:
            logger.error(f"Error while writing data to CSV: {e}")
            raise

    def save_csv(self, report_name: str, results: List[List[str]], headers: List[str]):
        try:
            logger.info(f"Saving CSV report to {report_name}")
            report_path = Path(report_name)
            # Check if the report name has a file extension, if not, add .csv extension
            if not report_path.suffix:
                report_path = report_path.with_suffix('.csv')

            with report_path.open(mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                self._write_header(csv_writer, headers)
                self._write_data(csv_writer, results)

        except PermissionError:
            logger.error(
                f"Permission denied: Unable to save the CSV report to {report_name}")
        except IOError as e:
            logger.error(f"IO Error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving the CSV report: {e}")

    def generate_csv_report(self, report_name: str, results: List[List[str]],
                            headers: List[str]):
        logger.info(f"Starting CSV report generation for {report_name}")
        self.save_csv(report_name, results, headers)
