# modules/portals/nc_portal.py
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.logger import logger

# Configuration settings for the North Carolina Business Search Portal
NC_PORTAL_CONFIG = {
    "url": "https://www.sosnc.gov/divisions/business_registration",  # URL of the NC Business Search Portal.
    "selectors": {
        "search_type": "select#CorpSearchType",  # CSS selector for the search type dropdown.
        "search_mode": "select#Words",  # CSS selector for the search mode dropdown.
        "search_input": "input#SearchCriteria",  # CSS selector for the search input field.
        "submit_button": "button#SubmitButton",  # CSS selector for the submit button.
        "results": "article#results-article span"  # CSS selector for the element showing search results.
    }
}


class NCPortal:
    # Class for interacting with the North Carolina Business Search Portal.

    def __init__(self, driver):
        self.driver = driver  # Initializing with a WebDriver instance.

    def check_availability(self, company_name):
        # Method to check the availability of a company name in the NC portal.
        logger.info(f"Received company name: {company_name}")
        try:
            self.driver.get(NC_PORTAL_CONFIG["url"])  # Navigating to the portal URL.
            logger.info(f"Accessing NC Business Search portal: {NC_PORTAL_CONFIG['url']}")

            # Selecting "CORPORATION" in the search type dropdown.
            search_type_select = Select(self.driver.find_element(By.ID, "CorpSearchType"))
            search_type_select.select_by_value("CORPORATION")

            # Setting the search mode to "Exact".
            search_mode = self.driver.find_element(By.CSS_SELECTOR, NC_PORTAL_CONFIG["selectors"]["search_mode"])
            search_mode.send_keys("Exact")

            # Clearing the search input and entering the company name.
            search_input = self.driver.find_element(By.CSS_SELECTOR, NC_PORTAL_CONFIG["selectors"]["search_input"])
            search_input.clear()
            search_input.send_keys(company_name)

            # Clicking the search button.
            search_button = self.driver.find_element(By.CSS_SELECTOR, NC_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            # Waiting for the results element to be present.
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, NC_PORTAL_CONFIG["selectors"]["results"])))

            # Checking the text in the results element.
            results_text = self.driver.find_element(By.CSS_SELECTOR, NC_PORTAL_CONFIG["selectors"]["results"]).text
            if "Records Found: 0" in results_text:
                logger.info(f"Company name '{company_name}' is available in NC.")
                return "Available"
            else:
                logger.info(f"Company name '{company_name}' is not available in NC.")
                return "Not Available"

        except NoSuchElementException as e:
            logger.error(f"Element not found in NC Business Search portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            logger.error(f"Timeout occurred in NC Business Search portal: {e}")
            return "Status Unknown"
