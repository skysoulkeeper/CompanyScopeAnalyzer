# modules/reporting/sql_writer.py
from utils.logger import logger
from typing import List


class SQLReportGenerator:
    def __init__(self, state_abbr: str):
        self.state_abbr = state_abbr

    def generate_sql_report(self, filename: str, results: List[List[str]]) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for result_lines in results:
                    company_name = self._parse_info(result_lines[0])[1]
                    bns_status = self._parse_info(result_lines[1])[1]
                    domain_data = result_lines[2:]

                    domain_columns = []
                    domain_values = []
                    for domain_info in domain_data:
                        domain_zone, domain_status = self._parse_info(domain_info)
                        domain_columns.append(domain_zone)
                        domain_values.append(self._escape_sql_value(domain_status))

                    columns = ['name', 'state', 'BNS'] + domain_columns
                    values = [self._escape_sql_value(value) for value in
                              [company_name, self.state_abbr,
                               bns_status]] + domain_values

                    sql_statement = f"INSERT INTO companies ({', '.join(columns)}) VALUES ({', '.join(values)})"
                    file.write(sql_statement + ";\n")

                file.write("\n")
        except Exception as e:
            logger.error(f"Error generating SQL report: {e}", exc_info=True)
            raise

    @staticmethod
    def _parse_info(info: str) -> (str, str):
        parts = info.split(': ')
        domain = parts[0].strip()
        zone = domain.split('.')[-1]
        return f".{zone}", parts[1].strip()

    @staticmethod
    def _escape_sql_value(value: str) -> str:
        return f"""'{value.replace("'", "''")}'"""
