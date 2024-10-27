# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/reporting/sql_writer.py

Description:
This module defines the SQLReportGenerator class, which generates SQL reports based
on the provided results. It formats the results into SQL INSERT statements, handling
company names, business name status, and domain data.
"""

from utils.logger import logger
from typing import List


class SQLReportGenerator:
    def __init__(self, state_abbr: str):
        self.state_abbr = state_abbr  # Storing the state abbreviation.

    def generate_sql_report(self, filename: str, results: List[List[str]]) -> None:
        # Method to generate an SQL report.
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                # Writing to the specified file.
                for result_lines in results:
                    # Parsing each line of results.
                    company_name = self._parse_info(result_lines[0])[1]  # Extracting the company name.
                    bns_status = self._parse_info(result_lines[1])[1]  # Extracting the business name status.
                    domain_data = result_lines[2:]  # Extracting the domain data.

                    domain_columns = []
                    domain_values = []
                    for domain_info in domain_data:
                        # Parsing each domain information line.
                        domain_zone, domain_status = self._parse_info(domain_info)
                        domain_columns.append(domain_zone)
                        domain_values.append(self._escape_sql_value(domain_status))

                    # Constructing the SQL INSERT statement columns and values.
                    columns = ['name', 'state', 'BNS'] + domain_columns
                    values = [self._escape_sql_value(value) for value in
                              [company_name, self.state_abbr, bns_status]] + domain_values

                    # Writing the SQL statement to the file.
                    sql_statement = f"INSERT INTO companies ({', '.join(columns)}) VALUES ({', '.join(values)})"
                    file.write(sql_statement + ";\n")

                file.write("\n")  # Adding a new line at the end of the file.
        except Exception as e:
            logger.error(f"Error generating SQL report: {e}", exc_info=True)
            raise

    @staticmethod
    def _parse_info(info: str) -> (str, str):
        # Static method to parse information from a string.
        parts = info.split(': ')
        domain = parts[0].strip()
        zone = domain.split('.')[-1]  # Extracting the domain zone (e.g., .com, .net).
        return f".{zone}", parts[1].strip()  # Returning the domain zone and the second part of the split.

    @staticmethod
    def _escape_sql_value(value: str) -> str:
        # Static method to escape SQL values.
        # Replacing single quotes in the string with double single quotes to prevent SQL injection.
        return f"""'{value.replace("'", "''")}'"""
