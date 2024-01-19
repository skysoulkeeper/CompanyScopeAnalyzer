# modules/portals/ga_portal.py
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class GAPortal:
    def __init__(self, driver):
        self.driver = driver

        self.config = {
            "url": "https://ecorp.sos.ga.gov/BusinessSearch",
            "selectors": {
                "exact_match_radio": "input#rdExactMatch",
                "search_input": "input#txtBusinessName",
                "search_button": "input#btnSearch",
                "error_message": "li.error_message",
                "company_status": "td"
            }
        }

    @staticmethod
    def format_company_name(name):
        name = name.upper()
        if "LLC" not in name and "INC" not in name:
            return name + " LLC"
        return name

    def check_availability(self, company_name):
        logger.info(f"Received company name: {company_name}")
        formatted_company_name = self.format_company_name(company_name)
        logger.info(f"Formatted company name: {formatted_company_name}")
        try:
            self.driver.get(self.config["url"])
            logger.info(f"Accessing GA portal: {self.config['url']}")

            exact_match_radio = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["exact_match_radio"])
            exact_match_radio.click()

            search_input = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["search_input"])
            search_input.clear()
            search_input.send_keys(formatted_company_name)

            search_button = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["search_button"])
            search_button.click()

            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["error_message"]) or
                               driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["company_status"])
            )

            error_messages = self.driver.find_elements(By.CSS_SELECTOR, self.config["selectors"]["error_message"])
            if any("No data found" in message.text for message in error_messages):
                logger.info(f"Company name '{formatted_company_name}' is available in GA.")
                return "Available"

            status_elements = self.driver.find_elements(By.CSS_SELECTOR, self.config["selectors"]["company_status"])
            for status_element in status_elements:
                if "Active" in status_element.text:
                    logger.info(f"Company name '{formatted_company_name}' is Active in GA.")
                    return "Not Available"

            logger.info(f"Company name '{formatted_company_name}' not found as Active in GA.")
            return "Not Found"

        except NoSuchElementException as e:
            logger.error(f"Element not found in GA portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            logger.error(f"Timeout occurred in GA portal: {e}")
            return "Status Unknown"
