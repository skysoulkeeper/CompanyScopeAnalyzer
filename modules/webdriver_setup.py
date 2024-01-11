# modules/webdriver_setup.py
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict


def setup_webdriver(config: Dict[str, any]) -> webdriver.Chrome:
    logger = logging.getLogger(__name__)
    logger.info("Setting up WebDriver")

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    if 'webdriver' not in config:
        raise KeyError("WebDriver configuration not found in config.")

    webdriver_config = config['webdriver']
    user_agent = webdriver_config.get('user_agent')
    implicit_wait_time = webdriver_config.get('implicit_wait_time')

    if user_agent is None or implicit_wait_time is None:
        raise KeyError("Missing required WebDriver configuration parameters.")

    options.add_argument(f"user-agent={user_agent}")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(implicit_wait_time)
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {e}")
        raise

    logger.info("WebDriver setup completed")
    return driver
