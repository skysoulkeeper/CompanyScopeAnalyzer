# modules/portals/md_portal.py
import time

from selenium.webdriver import ActionChains

from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configuration settings for the Maryland Business Express Entity Search
MD_PORTAL_CONFIG = {
    "url": "https://egov.maryland.gov/BusinessExpress/EntitySearch",
    "selectors": {
        "search_input": "input#BusinessName",
        "submit_button": "button#searchBus1",
        "business_radio": "input[name='SearchType'][value='BusinessName']",
        "not_found_message": "//div[contains(@class, 'textNotice') and contains(text(), 'The business name you entered was not found. Try your search again.')]"
    }
}


class MDPortal:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def format_company_name(name):
        name = name.upper()
        if "LLC" not in name and "INC" not in name:
            return name + " LLC"
        return name

    def type_like_human(self, element, text, delay=0.1):
        """ Type text into an element like a human """
        for character in text:
            element.send_keys(character)
            time.sleep(delay)

    def check_availability(self, company_name):
        logger.info(f"Received company name: {company_name}")
        formatted_company_name = self.format_company_name(company_name)
        logger.info(f"Formatted company name: {formatted_company_name}")
        try:
            # First, open Google and wait for a second
            self.driver.get("https://www.google.com")
            time.sleep(1)  # Wait for 1 second

            self.driver.get(MD_PORTAL_CONFIG["url"])
            logger.info(
                f"Accessing Maryland Business Express Entity Search: {MD_PORTAL_CONFIG['url']}")

            # Wait for the "DepartmentId" radio button to be present and then click it
            department_radio_selector = "input[name='SearchType'][value='DepartmentId']"
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, department_radio_selector)))
            department_radio = self.driver.find_element(By.CSS_SELECTOR,
                                                        department_radio_selector)
            actions = ActionChains(self.driver)
            actions.move_to_element(department_radio).click().perform()

            # Wait for the "BusinessName" radio button to be present and then click it
            business_radio_selector = "input[name='SearchType'][value='BusinessName']"
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, business_radio_selector)))
            business_radio = self.driver.find_element(By.CSS_SELECTOR,
                                                      business_radio_selector)
            actions = ActionChains(self.driver)
            actions.move_to_element(business_radio).click().perform()

            search_input = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, MD_PORTAL_CONFIG["selectors"]["search_input"])))
            search_input.clear()

            # Simulate human-like typing
            self.type_like_human(search_input, formatted_company_name)

            search_button = self.driver.find_element(By.CSS_SELECTOR,
                                                     MD_PORTAL_CONFIG["selectors"][
                                                         "submit_button"])
            actions = ActionChains(self.driver)
            actions.move_to_element(search_button).click().perform()

            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, MD_PORTAL_CONFIG["selectors"]["not_found_message"])))
            logger.info(f"Company name '{formatted_company_name}' is available in MD.")
            return "Available"
        except TimeoutException:
            logger.info(
                f"Company name '{formatted_company_name}' may not be available in MD.")
            return "Not Available"
        except NoSuchElementException as e:
            logger.error(
                f"Element not found in Maryland Business Express Entity Search: {e}")
            return "Status Unknown"
