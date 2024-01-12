# modules/reporting/xls_writer.py
import xlwt
import logging
from typing import List
from pathlib import Path
from utils.logger import setup_logging

# Setting up logging for this module
setup_logging()
logger = logging.getLogger(__name__)


class ExcelStyles:
    def __init__(self, workbook):
        self.wb = workbook
        self._setup_custom_colors()
        self._setup_styles()

    def _setup_custom_colors(self):
        # Define custom colors
        xlwt.add_palette_colour("custom_light_green", 0x21)
        self.wb.set_colour_RGB(0x21, 155, 194, 128)

        xlwt.add_palette_colour("custom_light_red", 0x22)
        self.wb.set_colour_RGB(0x22, 255, 204, 204)

        xlwt.add_palette_colour("custom_light_orange", 0x23)
        self.wb.set_colour_RGB(0x23, 255, 207, 160)

    def _setup_styles(self):
        # Define font styles
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.height = 15 * 20

        header_font = xlwt.Font()
        header_font.name = 'Times New Roman'
        header_font.bold = True
        header_font.height = 17 * 20

        # Define styles
        self.header_style = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;')
        self.header_style.font = header_font

        self.normal_style = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin;')
        self.normal_style.font = font

        self.red_style = xlwt.easyxf(
            'borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour custom_light_red;')
        self.red_style.font = font

        self.green_style = xlwt.easyxf(
            'borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour custom_light_green;')
        self.green_style.font = font

        self.orange_style = xlwt.easyxf(
            'borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour custom_light_orange;')
        self.orange_style.font = font


class XLSReportGenerator:
    def __init__(self, domain_zones: List[str]):
        self.domain_zones = domain_zones
        self.wb = xlwt.Workbook()
        self.styles = ExcelStyles(self.wb)  # Passing workbook to styles

    def _create_sheet(self):
        try:
            worksheet = self.wb.add_sheet('Results')
            headers = ["Company Name", "BNS Status"]
            for zone in self.domain_zones:
                headers.extend([zone, "Status"])
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, self.styles.header_style)
                worksheet.col(col_num).width = 256 * 20
            return worksheet, headers
        except Exception as e:
            logger.error(f"Error during sheet creation: {e}")
            raise

    def _write_data(self, worksheet, results: List[List[str]], headers: List[str]):
        logger.info("Writing data to the worksheet")
        try:
            for row_num, result_lines in enumerate(results, start=1):
                col_num = 0  # Start at the first column for each new row

                # Write Company Name
                company_name = result_lines[0].replace('Company: ', '')
                worksheet.write(row_num, col_num, company_name, self.styles.normal_style)
                col_num += 1

                # Write BNS Status without prefix
                bns_status = result_lines[1].split(': ')[1]
                cell_style = self.styles.red_style if 'Not Available' in bns_status else self.styles.green_style
                worksheet.write(row_num, col_num, bns_status, cell_style)
                col_num += 1

                # Write Domains and Statuses
                for domain_info in result_lines[2:]:
                    domain, status = domain_info.split(': ')
                    worksheet.write(row_num, col_num, domain, self.styles.normal_style)
                    col_num += 1

                    # Determine the style for the status based on whether it contains a price
                    cell_style = self.styles.orange_style if "$" in status else self.styles.normal_style
                    worksheet.write(row_num, col_num, status, cell_style)
                    col_num += 1

                # Adjust row height
                worksheet.row(row_num).height_mismatch = True
                worksheet.row(row_num).height = 20 * 40  # Set row height

        except Exception as e:
            logger.error(f"Error while writing data to the worksheet: {e}")
            raise

    def save_workbook(self, report_name: str):
        try:
            logger.info(f"Saving the workbook to {report_name}")
            report_path = Path(report_name)
            if not report_path.suffix:
                report_path = report_path.with_suffix('.xls')

            with report_path.open(mode='wb') as file:
                self.wb.save(file)
        except PermissionError:
            logger.error(f"Permission denied: Unable to save the workbook to {report_name}")
        except IOError as e:
            logger.error(f"IO Error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving the workbook: {e}")

    def write_report(self, report_name: str, results: List[List[str]]):
        logger.info(f"Starting report generation for {report_name}")
        ws, headers = self._create_sheet()
        self._write_data(ws, results, headers)
        self.save_workbook(report_name)


# Example usage
if __name__ == "__main__":
    try:
        report_generator = XLSReportGenerator([".com", ".net", ".org"])
        example_data = [
            ["Company: Company1", "BNS Status: Available", ".com: $9.99", ".net: Not Available", ".org: $14.99"],
            ["Company: Company2", "BNS Status: Not Available", ".com: Taken", ".net: Taken", ".org: Taken"]
        ]
        report_generator.write_report("example_report", example_data)
        logger.info("Report generated successfully.")
    except Exception as e:
        logger.error(f"Error while generating report: {e}")