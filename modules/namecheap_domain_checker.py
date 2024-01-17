# modules/namecheap_domain_checker.py
import time
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Define CSS selectors for elements on the Namecheap domain search page
SEARCH_INPUT = 'input#search-query'
SUBMIT_BUTTON = 'input[type="submit"]'


# Define a class for checking the availability of a domain on Namecheap
class DomainAvailabilityChecker:
    def __init__(self, driver, namecheap_url):
        # Initialize the checker with a WebDriver instance and Namecheap URL
        self.driver = driver
        self.namecheap_url = namecheap_url

    def check_domain_status(self, domain):
        try:
            # Navigate to the Namecheap URL for the given domain
            self.driver.get(self.namecheap_url + domain)
            logger.info(f"Accessing Namecheap for domain: {domain}")

            # Find the search input field and perform a search
            search_input = self.driver.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(domain + Keys.ENTER)
            time.sleep(2)

            # Extract the domain extension from the provided domain
            domain_extension = domain.split('.')[-1]
            domain_unavailable_selector = f'article.domain-{domain_extension}.unavailable'
            domain_available_selector = f'article.domain-{domain_extension}.available'

            try:
                # Wait for the "unavailable" message to appear (indicating the domain is taken)
                WebDriverWait(self.driver, 4).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, domain_unavailable_selector))
                )
                logger.info(f"Domain '{domain}' is not available.")
                return "Taken"
            except TimeoutException:
                try:
                    # Wait for the "available" message to appear (indicating the domain is available)
                    domain_article_available = WebDriverWait(self.driver, 4).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, domain_available_selector))
                    )
                    price_element = domain_article_available.find_element(
                        By.CSS_SELECTOR, 'div.price strong')
                    price = price_element.text
                    logger.info(f"Domain '{domain}' is available at {price}.")
                    return f"Available at {price}"
                except (NoSuchElementException, TimeoutException):
                    # Handle cases where the status of the domain is unknown
                    logger.info(f"Status of domain '{domain}' is unknown.")
                    return "Status Unknown"

        except NoSuchElementException as e:
            # Handle exceptions if elements are not found
            logger.error(f"Element not found: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            # Handle timeout exceptions
            logger.error(f"Timeout occurred: {e}")
            return "Status Unknown"
