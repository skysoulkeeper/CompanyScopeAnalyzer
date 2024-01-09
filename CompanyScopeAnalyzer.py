import logging
import time
import re
import yaml
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CompanyDomainChecker:
    def __init__(self):
        # Load configuration from config.yml
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
        self.check_company_name_availability = config['settings']['check_company_name_availability']
        self.check_company_domains = config['settings']['check_company_domains']
        self.njportal_url = config['settings']['njportal_url']
        self.namecheap_url = config['settings']['namecheap_url']
        self.domain_zones = config['settings']['domain_zones']
        self.logger = logging.getLogger(__name__)
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4896.60 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def format_company_name_to_domain(self, name):
        name = re.sub(r'\bLLC\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\bL\.L\.C\.\b', '', name, flags=re.IGNORECASE)
        formatted_name = re.sub(r'\s+', '', name)
        formatted_name = re.sub(r'[^a-zA-Z0-9]', '', formatted_name)
        return formatted_name.lower()

    def format_company_name_for_njportal(self, name):
        name = re.sub(r'\bLLC\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\bL\.L\.C\.\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\bINC\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\bI\.N\.C\.\b', '', name, flags=re.IGNORECASE)
        return name.strip()

    def check_company_availability(self, original_company_name):
        company_name = self.format_company_name_for_njportal(original_company_name)
        self.driver.get(self.njportal_url)
        search_input = self.driver.find_element(By.ID, "BusinessName")
        search_input.clear()
        search_input.send_keys(company_name)
        search_button = self.driver.find_element(By.XPATH, "//input[@type='submit'][@class='btn btn-warning']")
        search_button.click()
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, "//div[@class='alert alert-error']")
            return "Not Available"
        except NoSuchElementException:
            try:
                self.driver.find_element(By.XPATH, "//div[@class='alert alert-success']")
                return "Available"
            except NoSuchElementException:
                return "Status Unknown"

    def run(self):
        with open('company.txt', 'r') as file:
            companies = file.readlines()

        current_date = datetime.now().strftime("%d_%m_%Y")
        result_filename = f"result_{current_date}.txt"
        with open(result_filename, 'w', encoding='utf-8') as result_file:
            for company in companies:
                company_name = company.strip()
                formatted_name = self.format_company_name_to_domain(company_name)
                result_lines = [f"Company: {company_name}"]

                if self.check_company_name_availability.lower() == "yes":
                    nj_bns_status = self.check_company_availability(company_name)
                    result_lines.append(f"NJ BNS Status: {nj_bns_status}")

                if self.check_company_domains.lower() == "yes":
                    self.driver.get(self.namecheap_url)
                    for domain_extension in self.domain_zones:
                        full_domain = formatted_name + domain_extension
                        search_input = self.driver.find_element(By.ID, 'search-query')
                        search_input.clear()
                        search_input.send_keys(full_domain + Keys.ENTER)
                        time.sleep(2)

                        try:
                            WebDriverWait(self.driver, 4).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, f'article.domain-{domain_extension[1:]}.unavailable'))
                            )
                            result_lines.append(f"{full_domain}: Taken")
                        except TimeoutException:
                            try:
                                domain_article_available = WebDriverWait(self.driver, 4).until(
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'article.domain-{domain_extension[1:]}.available'))
                                )
                                price_element = domain_article_available.find_element(By.CSS_SELECTOR, 'div.price strong')
                                price = price_element.text
                                result_lines.append(f"{full_domain}: {price}")
                            except (NoSuchElementException, TimeoutException):
                                result_lines.append(f"{full_domain}: Not Available")

                for line in result_lines:
                    result_file.write(line + "\n")
                result_file.write("\n")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    checker = CompanyDomainChecker()
    checker.run()
    checker.close()
