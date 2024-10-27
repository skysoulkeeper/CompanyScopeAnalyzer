# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/reporting/json_writer.py

Description:
This module defines the JSONReportGenerator class, which handles the creation of
JSON reports. It allows adding data as dictionaries to an internal list and
saves the list to a JSON file with proper formatting.
"""

import json
from pathlib import Path
from utils.logger import logger


# Define a class for generating JSON reports
class JSONReportGenerator:
    def __init__(self):
        self.data = []

    def add_data(self, data_dict):
        # Add data in the form of a dictionary to the internal data list
        self.data.append(data_dict)

    def save_json(self, report_name):
        try:
            # Check if the report name has a file extension, if not, add .json extension
            logger.info(f"Saving JSON report to {report_name}")
            report_path = Path(report_name)
            if not report_path.suffix:
                report_path = report_path.with_suffix('.json')

            with report_path.open(mode='w', encoding='utf-8') as file:
                # Serialize the data list to JSON format and save it to the file
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except PermissionError:
            logger.error(f"Permission denied: Unable to save the JSON report to {report_name}")
        except IOError as e:
            logger.error(f"IO Error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving the JSON report: {e}")
