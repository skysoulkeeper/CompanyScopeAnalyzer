# modules/portals/ga_portal.py
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class GAPortal:
    def __init__(self, driver):
        self.driver = driver  # Initializing with a WebDriver instance to control the browser.

        # Configuration settings for the Georgia portal, including URL and CSS selectors.
        self.config = {
            "url": "https://ecorp.sos.ga.gov/BusinessSearch",
            "selectors": {
                "exact_match_radio": "input#rdExactMatch",  # CSS selector for the exact match radio button.
                "search_input": "input#txtBusinessName",  # CSS selector for the business name search input.
                "search_button": "input#btnSearch",  # CSS selector for the search button.
                "error_message": "li.error_message",  # CSS selector for any error message that might appear.
                "company_status": "td"  # CSS selector for elements containing company statuses.
            }
        }

    @staticmethod
    def format_company_name(name):
        # Static method for formatting company names.
        name = name.upper()  # Converts the name to uppercase.
        # Appends " LLC" if the name doesn't already end with "LLC" or "INC".
        if "LLC" not in name and "INC" not in name:
            return name + " LLC"
        return name

    def check_availability(self, company_name):
        # Method to check the availability of a company name in the Georgia portal.
        logger.info(f"Received company name: {company_name}")
        formatted_company_name = self.format_company_name(company_name)  # Formatting the company name.
        logger.info(f"Formatted company name: {formatted_company_name}")
        try:
            self.driver.get(self.config["url"])  # Navigating to the Georgia portal URL.
            logger.info(f"Accessing GA portal: {self.config['url']}")

            # Selecting the exact match radio button.
            exact_match_radio = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["exact_match_radio"])
            exact_match_radio.click()

            # Clearing the search input and entering the formatted company name.
            search_input = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["search_input"])
            search_input.clear()
            search_input.send_keys(formatted_company_name)

            # Clicking the search button.
            search_button = self.driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["search_button"])
            search_button.click()

            # Waiting for either an error message or a status element to appear.
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["error_message"]) or
                               driver.find_element(By.CSS_SELECTOR, self.config["selectors"]["company_status"])
            )

            # Checking for "No data found" error messages.
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, self.config["selectors"]["error_message"])
            if any("No data found" in message.text for message in error_messages):
                logger.info(f"Company name '{formatted_company_name}' is available in GA.")
                return "Available"

            # Checking if any of the status elements contain the word "Active".
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
