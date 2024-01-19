# modules/portals/fl_portal.py
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuration settings for the Florida Sunbiz Portal
FL_PORTAL_CONFIG = {
    "url": "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName",
    "selectors": {
        "search_input": "input#SearchTerm",
        "submit_button": "input[type='submit']",
        "company_name": "td.large-width a",
        "company_status": "td.small-width"
    }
}


class FLPortal:

    def __init__(self, driver):
        self.driver = driver

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
            self.driver.get(FL_PORTAL_CONFIG["url"])
            logger.info(f"Accessing FL Sunbiz portal: {FL_PORTAL_CONFIG['url']}")

            search_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["search_input"])))
            search_input.clear()
            search_input.send_keys(formatted_company_name)

            search_button = self.driver.find_element(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_name"])))

            companies = self.driver.find_elements(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_name"])
            statuses = self.driver.find_elements(By.CSS_SELECTOR, FL_PORTAL_CONFIG["selectors"]["company_status"])

            for comp, status in zip(companies, statuses):
                comp_name = comp.text.strip().upper()
                status_text = status.text.strip()
                if comp_name == formatted_company_name:
                    if status_text.lower() == "active":
                        logger.info(
                            f"Company name '{formatted_company_name}' is Active in FL.")
                        return "Not Available"
            logger.info(
                f"Company name '{formatted_company_name}' not found as Active in FL.")
            return "Available"

        except NoSuchElementException as e:
            logger.error(f"Element not found in FL Sunbiz portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            logger.error(f"Timeout occurred in FL Sunbiz portal: {e}")
            return "Status Unknown"
