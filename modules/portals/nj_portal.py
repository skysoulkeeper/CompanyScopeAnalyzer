# modules/portals/nj_portal.py
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuration settings for the NJ Portal
NJ_PORTAL_CONFIG = {
    "url": "https://www.njportal.com/DOR/BusinessNameSearch/Search/Availability",
    "selectors": {
        "search_input": "input#BusinessName",
        "submit_button": "input[type='submit'].btn.btn-warning",
        "alert": ".alert",
        "alert_error": ".alert.alert-error",
        "alert_success": ".alert.alert-success"
    }
}


# Define a class for the NJ Portal
class NJPortal:
    def __init__(self, driver):
        self.driver = driver

    def check_availability(self, company_name):
        try:
            # Navigate to the NJ Portal URL
            self.driver.get(NJ_PORTAL_CONFIG["url"])
            logger.info(f"Accessing NJ portal: {NJ_PORTAL_CONFIG['url']}")
            # Find and interact with elements on the NJ Portal page
            search_input = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["search_input"]))
            )
            search_input.clear()
            search_input.send_keys(company_name)

            search_button = self.driver.find_element(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert"])))

            # Check for success or error alerts on the NJ Portal page
            if self.driver.find_elements(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert_error"]):
                logger.info(f"Company name '{company_name}' is not available in NJ.")
                return "Not Available"
            elif self.driver.find_elements(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert_success"]):
                logger.info(f"Company name '{company_name}' is available in NJ.")
                return "Available"
            else:
                logger.info(f"Status of company name '{company_name}' is unknown in NJ.")
                return "Status Unknown"

        except NoSuchElementException as e:
            logger.error(f"Element not found in NJ portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            logger.error(f"Timeout occurred in NJ portal: {e}")
            return "Status Unknown"
