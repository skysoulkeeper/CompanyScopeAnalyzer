# modules/reporting/json_writer.py
import json
from pathlib import Path
from utils.logger import logger


class JSONReportGenerator:
    def __init__(self):
        self.data = []

    def add_data(self, data_dict):
        self.data.append(data_dict)

    def save_json(self, report_name):
        try:
            logger.info(f"Saving JSON report to {report_name}")
            report_path = Path(report_name)
            if not report_path.suffix:
                report_path = report_path.with_suffix('.json')

            with report_path.open(mode='w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except PermissionError:
            logger.error(f"Permission denied: Unable to save the JSON report to {report_name}")
        except IOError as e:
            logger.error(f"IO Error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving the JSON report: {e}")
