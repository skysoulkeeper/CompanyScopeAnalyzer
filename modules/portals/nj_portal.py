# modules/portals/nj_portal.py
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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


class NJPortal:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def check_availability(self, company_name):
        try:
            self.driver.get(NJ_PORTAL_CONFIG["url"])
            self.logger.info(f"Accessing NJ portal: {NJ_PORTAL_CONFIG['url']}")

            search_input = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["search_input"]))
            )
            search_input.clear()
            search_input.send_keys(company_name)

            search_button = self.driver.find_element(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert"])))
            if self.driver.find_elements(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert_error"]):
                self.logger.info(f"Company name '{company_name}' is not available in NJ.")
                return "Not Available"
            elif self.driver.find_elements(By.CSS_SELECTOR, NJ_PORTAL_CONFIG["selectors"]["alert_success"]):
                self.logger.info(f"Company name '{company_name}' is available in NJ.")
                return "Available"
            else:
                self.logger.info(f"Status of company name '{company_name}' is unknown in NJ.")
                return "Status Unknown"

        except NoSuchElementException as e:
            self.logger.error(f"Element not found in NJ portal: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            self.logger.error(f"Timeout occurred in NJ portal: {e}")
            return "Status Unknown"
