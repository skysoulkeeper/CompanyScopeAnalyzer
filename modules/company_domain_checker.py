# modules/company_domain_checker.py
import logging
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Новые константы селекторов, основанные на старом коде
SEARCH_INPUT = 'input#search-query'
SUBMIT_BUTTON = 'input[type="submit"]'
# Динамические селекторы, базирующиеся на расширении домена
# DOMAIN_UNAVAILABLE и DOMAIN_AVAILABLE будут формироваться динамически в методе

class CompanyDomainChecker:
    def __init__(self, driver, namecheap_url):
        self.driver = driver
        self.namecheap_url = namecheap_url
        self.logger = logging.getLogger(__name__)

    def check_domain_status(self, domain):
        try:
            self.driver.get(self.namecheap_url + domain)
            self.logger.info(f"Accessing Namecheap for domain: {domain}")

            search_input = self.driver.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(domain + Keys.ENTER)
            time.sleep(2)

            domain_extension = domain.split('.')[-1]
            domain_unavailable_selector = f'article.domain-{domain_extension}.unavailable'
            domain_available_selector = f'article.domain-{domain_extension}.available'

            try:
                WebDriverWait(self.driver, 4).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, domain_unavailable_selector))
                )
                self.logger.info(f"Domain '{domain}' is not available.")
                return "Taken"
            except TimeoutException:
                try:
                    domain_article_available = WebDriverWait(self.driver, 4).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, domain_available_selector))
                    )
                    price_element = domain_article_available.find_element(By.CSS_SELECTOR, 'div.price strong')
                    price = price_element.text
                    self.logger.info(f"Domain '{domain}' is available at {price}.")
                    return f"Available at {price}"
                except (NoSuchElementException, TimeoutException):
                    self.logger.info(f"Status of domain '{domain}' is unknown.")
                    return "Status Unknown"

        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e}")
            return "Status Unknown"
        except TimeoutException as e:
            self.logger.error(f"Timeout occurred: {e}")
            return "Status Unknown"
