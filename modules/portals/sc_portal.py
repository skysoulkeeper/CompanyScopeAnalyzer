# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/portals/sc_portal.py

Description:
This module defines the SCPortal class, which interacts with the South Carolina
Business Filing portal to check the availability of company names.
The module automates the search process using Selenium WebDriver, processes
the results, and manages browser instances to maintain session integrity.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from utils.logger import logger

# Configuration settings for the SC Portal
SC_PORTAL_CONFIG = {
    "url": "https://businessfilings.sc.gov/BusinessFiling/Entity/Search",  # URL of the SC Business Filing Portal.
    "selectors": {
        "search_type_dropdown": "select#EntitySearchTypeEnumId",  # CSS selector for the search type dropdown.
        "search_input": "input#SearchTextBox",  # CSS selector for the search input.
        "submit_button": "button#EntitySearchButton",  # CSS selector for the submit button.
        "name_availability_message": "div#nameAvailabilityDiv p.alert",  # CSS selector for the name availability message.
        "recaptcha": "div.g-recaptcha"  # CSS selector for the reCAPTCHA element.
    }
}


class SCPortal:
    def __init__(self, driver=None):
        # Constructor for the SCPortal class.
        self.driver = driver if driver is not None else webdriver.Chrome()  # Initializing the WebDriver.
        self.check_count = 0  # Counter to track the number of checks performed.

    def check_availability(self, company_name):
        # Method to check the availability of a company name in the SC portal.
        logger.info(f"Checking availability of company name: {company_name}")
        try:
            self.driver.get(SC_PORTAL_CONFIG["url"])  # Navigating to the SC Portal URL.
            time.sleep(1)  # Short pause to ensure page loads properly.

            # Selecting 'Exact Match' from the dropdown menu.
            search_type_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["search_type_dropdown"]))
            )
            search_type_select.send_keys("Exact Match")
            time.sleep(1)  # Short pause after selection.

            # Entering the company name into the search input.
            search_input = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["search_input"])
            search_input.clear()
            search_input.send_keys(company_name)
            time.sleep(1)  # Short pause after entering the name.

            # Clicking the search button.
            search_button = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            # Waiting for the availability message to appear.
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["name_availability_message"]))
                )
                availability_message = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["name_availability_message"]).text.lower()
            except TimeoutException:
                logger.error("Timeout while waiting for the availability message.")
                return "Timeout/Error"

            # Interpreting the availability message.
            if "this name is available" in availability_message:
                logger.info(f"Company name '{company_name}' is available in SC.")
                return "Available"
            else:
                logger.info(f"Company name '{company_name}' may not be available in SC.")
                return "Not Available"

        except Exception as e:
            logger.error(f"Error occurred in SC portal: {e}")
            return "Error"

        finally:
            self.check_count += 1  # Incrementing the check counter.

            # Restarting the browser after every 3 checks to avoid potential issues.
            if self.check_count % 3 == 0:
                self.driver.quit()  # Closing the browser.
                time.sleep(5)  # Pausing before restarting.
                self.driver = webdriver.Chrome()  # Restarting the browser.

