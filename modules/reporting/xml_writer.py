# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/reporting/xml_writer.py

Description:
This module defines the XMLReportGenerator class, which generates XML reports based on the provided data.
It creates an XML file with structured elements representing company information, including domain status
and business name status.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
from utils.logger import logger


class XMLReportGenerator:
    def __init__(self, file_name: str, state: str):
        self.file_name = file_name  # Name of the XML file to be created.
        self.state = state  # State information to be included in the XML report.

    def write_to_xml(self, data: List[List[str]]):
        # Method to write provided data into an XML file.
        logger.info("Beginning data recording into XML file")
        root = ET.Element("Companies")  # Creating the root element 'Companies'.

        for result_lines in data:
            # Creating a 'Company' sub-element for each company in the data.
            company_elem = ET.SubElement(root, "Company")
            for line in result_lines:
                try:
                    if ":" not in line:
                        tag = "Domain"  # Default tag for lines without ':'.
                        text = line
                    else:
                        # Splitting the line into tag and text.
                        parts = line.split(": ", 1)
                        tag = parts[0].strip()
                        text = parts[1].strip() if len(parts) > 1 else ""
                        # Replacing specific strings in tags and texts.
                        tag = tag.replace("Company", "").replace("BNS Status", "BNSStatus")
                        text = text.replace("Company: ", "").replace("BNS status: ", "")

                    # Adding the tag and text to the company element.
                    ET.SubElement(company_elem, tag or "Name").text = text
                except ValueError as e:
                    logger.error(f"Error in data format '{line}': {e}")

        try:
            # Generating the XML tree and saving it to a file.
            tree = ET.ElementTree(root)
            xml_file_path = Path(f"{self.file_name}.xml")  # Defining the file path.
            tree.write(xml_file_path)  # Writing the XML tree to the file.
            logger.info(f"XML file successfully saved: {xml_file_path}")
        except ET.ParseError as e:
            logger.error(f"Error while generating XML: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving XML file: {e}")


# Example usage
if __name__ == "__main__":
    # Creating an instance of XMLReportGenerator and writing sample data to an XML file.
    xml_writer = XMLReportGenerator("report", state="NJ")
    sample_data = [["Company: Company1", "Status: Active"], ["Company: Company2", "Status: Inactive"]]
    xml_writer.write_to_xml(sample_data)
