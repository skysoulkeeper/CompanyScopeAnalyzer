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
                    company_name = self._parse_info(result_lines[0])
                    bns_status = self._parse_info(result_lines[1])
                    domain_data = result_lines[2:]

                    values = [self._escape_sql_value(value) for value in
                              [company_name, self.state_abbr, bns_status]]
                    domain_values = [self._escape_sql_value(self._parse_info(info, 1))
                                     for info in domain_data]
                    values.extend(domain_values)

                    columns = ['name', 'state', 'BNS'] + [self._parse_info(info, -1) for
                                                          info in domain_data]
                    sql_statement = f"INSERT INTO companies ({', '.join(columns)}) VALUES ({', '.join(values)})"
                    file.write(sql_statement + ";\n")
                file.write("\n")
        except Exception as e:
            logger.error(f"Error generating SQL report: {e}", exc_info=True)
            raise

    @staticmethod
    def _parse_info(info: str, index: int = 1) -> str:
        return info.split(': ')[index].strip()

    @staticmethod
    def _escape_sql_value(value: str) -> str:
        return f"""'{value.replace("'", "''")}'"""
