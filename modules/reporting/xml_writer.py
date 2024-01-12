# modules/reporting/xml_writer.py
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import List
from utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class XMLReportGenerator:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def write_to_xml(self, data: List[List[str]]):
        logger.info("Beginning data recording into XML file")
        root = ET.Element("Companies")

        for result_lines in data:
            company_elem = ET.SubElement(root, "Company")
            for line in result_lines:
                try:
                    tag, text = line.split(": ")
                    ET.SubElement(company_elem, tag.replace(" ", "")).text = text
                except ValueError as e:
                    logger.error(f"Error in data format '{line}': {e}")

        try:
            tree = ET.ElementTree(root)
            xml_file_path = Path(f"{self.file_name}.xml")
            tree.write(xml_file_path)
            logger.info(f"XML file successfully saved: {xml_file_path}")
        except ET.ParseError as e:
            logger.error(f"Error while generating XML: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving XML file: {e}")


# Example usage
if __name__ == "__main__":
    xml_writer = XMLReportGenerator("report")
    data = [["Company: Company1", "Status: Active"],
            ["Company: Company2", "Status: Inactive"]]
    xml_writer.write_to_xml(data)
