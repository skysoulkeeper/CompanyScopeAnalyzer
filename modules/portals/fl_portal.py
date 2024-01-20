# modules/portals/fl_portal.py
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuration settings for the Florida Sunbiz Portal
FL_PORTAL_CONFIG = {
    "url": "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName",  # URL of the Florida Sunbiz Portal.
    "selectors": {
        "search_input": "input#SearchTerm",  # CSS selector for the search input field.
        "submit_button": "input[type='submit']",  # CSS selector for the search submit button.
        "company_name": "td.large-width a",  # CSS selector for elements containing company names.
        "company_status": "td.small-width"  # CSS selector for elements containing company statuses.
    }
}


class FLPortal:
    # Class representing the Florida Sunbiz Portal.

    def __init__(self, driver):
        self.driver = driver  # Initializing the class with a WebDriver instance.

    @staticmethod
    def format_company_name(name):
        # Static method to format company names.
        name = name.upper()  # Converts the name to uppercase.
        # Adds " LLC" to the name if it doesn't already end with "LLC" or "INC".
        if "LLC" not in name and "INC" not in name:
            return name + " LLC"
        return name

    def check_availability(self, company_name):
        # Method to check the availability of a company name.
        logger.info(f"Received company name: {company_name}")
        formatted_company_name = self.format_company_name(company_name)  # Formatting the company name.
        logger.info(f"Formatted company name: {formatted_company_name}")
        try:
            self.driver.get(FL_PORTAL_CONFIG["url"])  # Navigating to the portal URL.
            logger.info(f"Accessing FL Sunbiz portal: {FL_PORTAL_CONFIG['url']}")

            # Waiting for the search input to be present and then clearing it and entering the formatted company name.
            search_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["search_input"])))
            search_input.clear()
            search_input.send_keys(formatted_company_name)

            # Finding and clicking the search button.
            search_button = self.driver.find_element(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            # Waiting for the company name elements to be present.
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_name"])))

            # Retrieving a list of companies and their statuses.
            companies = self.driver.find_elements(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_name"])
            statuses = self.driver.find_elements(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_status"])

            # Checking if the formatted company name matches any active company.
            for comp, status in zip(companies, statuses):
                comp_name = comp.text.strip().upper()
                status_text = status.text.strip()
                if comp_name == formatted_company_name:
                    if status_text.lower() == "active":
                        logger.info(f"Company name '{formatted_company_name}' is Active in FL.")
                        return "Not Available"
            logger.info(f"Company name '{formatted_company_name}' not found as Active in FL.")
            return "Available"

        except NoSuchElementException as e:
            logger.error(f"Element not found in FL Sunbiz portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            logger.error(f"Timeout occurred in FL Sunbiz portal: {e}")
            return "Status Unknown"
