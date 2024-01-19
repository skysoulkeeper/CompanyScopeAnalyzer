from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from utils.logger import logger

# Configuration settings for the SC Portal
SC_PORTAL_CONFIG = {
    "url": "https://businessfilings.sc.gov/BusinessFiling/Entity/Search",
    "selectors": {
        "search_type_dropdown": "select#EntitySearchTypeEnumId",
        "search_input": "input#SearchTextBox",
        "submit_button": "button#EntitySearchButton",
        "name_availability_message": "div#nameAvailabilityDiv p.alert",
        "recaptcha": "div.g-recaptcha"
    }
}

class SCPortal:
    def __init__(self, driver=None):
        self.driver = driver if driver is not None else webdriver.Chrome()
        self.check_count = 0  # Счетчик для отслеживания количества проверок

    def check_availability(self, company_name):
        logger.info(f"Checking availability of company name: {company_name}")
        try:
            # Навигация к SC Portal URL
            self.driver.get(SC_PORTAL_CONFIG["url"])
            time.sleep(1)

            # Выбор 'Exact Match' из выпадающего списка
            search_type_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["search_type_dropdown"]))
            )
            search_type_select.send_keys("Exact Match")
            time.sleep(1)

            # Ввод названия компании
            search_input = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["search_input"])
            search_input.clear()
            search_input.send_keys(company_name)
            time.sleep(1)

            # Нажатие кнопки поиска
            search_button = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["submit_button"])
            search_button.click()

            # Ожидание появления сообщения о доступности
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["name_availability_message"]))
                )
                availability_message = self.driver.find_element(By.CSS_SELECTOR, SC_PORTAL_CONFIG["selectors"]["name_availability_message"]).text.lower()
            except TimeoutException:
                logger.error("Timeout while waiting for the availability message.")
                return "Timeout/Error"

            # Проверка сообщения о доступности
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
            # Увеличение счетчика проверок
            self.check_count += 1

            # Если проверено 3 компании, закрыть и переоткрыть браузер
            if self.check_count % 3 == 0:
                self.driver.quit()
                time.sleep(5)  # Пауза перед перезапуском
                self.driver = webdriver.Chrome()  # Перезапуск браузера


