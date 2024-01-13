# modules/reporting/report_generator.py
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from modules.reporting.xls_writer import XLSReportGenerator
from modules.reporting.xml_writer import XMLReportGenerator
from modules.reporting.json_writer import JSONReportGenerator
from modules.reporting.csv_writer import CSVReportGenerator
from utils.logger import logger


class ReportGenerator:
    def __init__(self, config_params: Dict[str, any], results_list: List[List[str]],
                 state_abbr: str):
        self.config_data = config_params
        self.state_abbr = state_abbr
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
            'txt': self._generate_txt_report,
            'csv': self._generate_csv_report,
            'sql': self._generate_sql_report
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
            state_abbr = self.config_data.get('state_portal_abbr', 'Unknown')
            report_generator = XLSReportGenerator(self.config_data['domain_zones'],
                                                  state_abbr)
            report_generator.write_report(str(self.report_filename), self.result_data)
        except Exception as e:
            logger.error(f"Error generating XLS report: {e}")
            raise

    def _generate_csv_report(self):
        try:
            logger.info("Generating CSV report.")
            csv_filename = f"{str(self.report_filename)}.csv"
            state = self.config_data.get('state_portal_abbr', 'Unknown')
            headers = ["Company", "State", "BNS Status"] + self.config_data.get(
                'domain_zones', [])  # Заголовки для CSV
            csv_report_generator = CSVReportGenerator(
                self.config_data.get('domain_zones', []), state)
            csv_report_generator.generate_csv_report(csv_filename, self.result_data,
                                                     headers)
        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")
            raise

    def _generate_json_report(self):
        try:
            logger.info("Generating JSON report.")
            state = self.config_data.get('state_portal_abbr', 'Unknown')
            json_generator = JSONReportGenerator()

            for result_lines in self.result_data:
                data_dict = {
                    "Company": result_lines[0].replace('Company: ', ''),
                    "State": state,
                    "BNS status": result_lines[1].split(': ')[1],
                    "Domains": {}
                }
                for domain_info in result_lines[2:]:
                    domain, status = domain_info.split(': ', 1)
                    data_dict["Domains"][domain.strip()] = status.strip()
                json_generator.add_data(data_dict)
            json_generator.save_json(self.report_filename.with_suffix('.json'))
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            raise

    def _generate_sql_report(self):
        try:
            logger.info("Generating SQL report.")
            sql_filename = f"{str(self.report_filename)}.sql"

            with open(sql_filename, 'w', encoding='utf-8') as file:
                for result_lines in self.result_data:
                    # Разделение данных по колонкам
                    company_name = result_lines[0].split(': ', 1)[1]
                    bns_status = result_lines[1].split(': ', 1)[1]
                    domain_data = result_lines[2:]

                    # Сформировать список значений
                    values = [f"'{company_name}'", f"'{self.state_abbr}'",
                              f"'{bns_status}'"]
                    for domain_info in domain_data:
                        domain_zone, status = domain_info.split(': ')
                        domain_zone = domain_zone.split('.')[
                            -1]  # Получение только доменной зоны
                        values.append(f"'{status}'")

                    # Сформировать список колонок
                    columns = ['name', 'state', 'BNS'] + [domain.split('.')[-1] for
                                                          domain, _ in
                                                          [d.split(': ') for d in
                                                           domain_data]]

                    # Создать SQL-запрос
                    sql_statement = f"INSERT INTO companies ({', '.join(columns)}) VALUES ({', '.join(values)})"
                    file.write(sql_statement + ";\n")
                file.write("\n")
        except Exception as e:
            logger.error(f"Error generating SQL report: {e}")
            raise

    def _generate_xml_report(self):
        try:
            logger.info("Generating XML report.")
            state = self.config_data.get('state_portal_abbr',
                                         'Unknown')
            xml_writer = XMLReportGenerator(str(self.report_filename), state=state)
            modified_data = [
                [f"Company: {line[0]}",
                 f"State: {state}",
                 f"BNS Status: {line[1]}",
                 *line[2:]] for line in self.result_data]

            xml_writer.write_to_xml(modified_data)
        except Exception as e:
            logger.error(f"Error generating XML report: {e}")
            raise

    def _generate_txt_report(self):
        try:
            logger.info("Generating TXT report.")
            txt_filename = f"{str(self.report_filename)}.txt"
            state = self.config_data.get('state_portal_abbr', 'Unknown')

            with open(txt_filename, 'w', encoding='utf-8') as file:
                for result_lines in self.result_data:
                    file.write(result_lines[0] + "\n")
                    file.write(f"State: {state}\n")
                    for line in result_lines[1:]:
                        file.write(line + "\n")
                    file.write("\n")
        except Exception as e:
            logger.error(f"Error generating TXT report: {e}")
            raise


# Example usage
if __name__ == "__main__":
    config_data = {}
    result_data = []
    state_abbr = config_data.get('state_portal_abbr', 'Unknown')
    report_gen = ReportGenerator(config_data, result_data)
    report_gen.generate_report()
