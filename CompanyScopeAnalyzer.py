import logging
import time
import re
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

# Format company name for domain checking
def format_company_name_to_domain(name):
    name = re.sub(r'\bLLC\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\bL\.L\.C\.\b', '', name, flags=re.IGNORECASE)
    formatted_name = re.sub(r'\s+', '', name)
    formatted_name = re.sub(r'[^a-zA-Z0-9]', '', formatted_name)
    return formatted_name.lower()

# Format company name for company name checking
def format_company_name_for_njportal(name):
    name = re.sub(r'\bLLC\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\bL\.L\.C\.\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\bINC\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\bI\.N\.C\.\b', '', name, flags=re.IGNORECASE)
    return name.strip()

# Check company name availability on NJPortal
def check_company_availability(driver, original_company_name, njportal_url):
    company_name = format_company_name_for_njportal(original_company_name)
    driver.get(njportal_url)
    search_input = driver.find_element(By.ID, "BusinessName")
    search_input.clear()
    search_input.send_keys(company_name)
    search_button = driver.find_element(By.XPATH, "//input[@type='submit'][@class='btn btn-warning']")
    search_button.click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//div[@class='alert alert-error']")
        return "Not Available"
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, "//div[@class='alert alert-success']")
            return "Available"
        except NoSuchElementException:
            return "Status Unknown"

def main():
    # Settings
    check_company_name_availability = "yes"
    check_company_domains = "yes"
    njportal_url = "https://www.njportal.com/DOR/BusinessNameSearch/Search/Availability"
    namecheap_url = "https://www.namecheap.com/domains/registration/results/?domain="
    domain_zones = [".com", ".net"]

    # Logger setup
    logger = logging.getLogger(__name__)

    # WebDriver setup
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4896.60 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    # Start WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    # Read company list from file
    with open('company.txt', 'r') as file:
        companies = file.readlines()

    # Create results file
    current_date = datetime.now().strftime("%d_%m_%Y")
    result_filename = f"result_{current_date}.txt"
    with open(result_filename, 'w', encoding='utf-8') as result_file:
        for company in companies:
            company_name = company.strip()
            formatted_name = format_company_name_to_domain(company_name)
            result_lines = [f"Company: {company_name}"]

            # Check company name availability
            if check_company_name_availability.lower() == "yes":
                nj_bns_status = check_company_availability(driver, company_name, njportal_url)
                result_lines.append(f"NJ BNS Status: {nj_bns_status}")

            # Domain checking
            if check_company_domains.lower() == "yes":
                driver.get(namecheap_url)
                for domain_extension in domain_zones:
                    full_domain = formatted_name + domain_extension
                    search_input = driver.find_element(By.ID, 'search-query')
                    search_input.clear()
                    search_input.send_keys(full_domain + Keys.ENTER)
                    time.sleep(2)
                    try:
                        WebDriverWait(driver, 4).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, f'article.domain-{domain_extension[1:]}.unavailable'))
                        )
                        result_lines.append(f"{full_domain}: Taken")
                    except TimeoutException:
                        try:
                            domain_article_available = WebDriverWait(driver, 4).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, f'article.domain-{domain_extension[1:]}.available'))
                            )
                            price_element = domain_article_available.find_element(By.CSS_SELECTOR, 'div.price strong')
                            price = price_element.text
                            result_lines.append(f"{full_domain}: {price}")
                        except (NoSuchElementException, TimeoutException):
                            result_lines.append(f"{full_domain}: Not Available")

            # Write results to file
            for line in result_lines:
                result_file.write(line + "\n")
            result_file.write("\n")

    # Close browser
    driver.quit()

if __name__ == "__main__":
    main()
