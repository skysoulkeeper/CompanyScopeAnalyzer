# modules/webdriver_setup.py
import json
from utils.logger import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict


def setup_webdriver(config: Dict[str, any]) -> webdriver.Chrome:
    # Extract proxy and webdriver configuration
    proxy_settings = config.get('proxy_settings', {})
    webdriver_config = config.get('webdriver', {})

    # Log the proxy and webdriver configuration before setting up the WebDriver
    logger.info("Proxy Settings: {}", json.dumps(proxy_settings))
    logger.info("Webdriver Configuration: {}", json.dumps(webdriver_config))

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-cookies")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("accept-encoding=gzip, deflate, br")
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

    # Proxy Configuration
    if 'proxy_settings' in config and config['proxy_settings'].get('proxy_enabled'):
        proxy_host = config['proxy_settings'].get('proxy_host')
        proxy_port = config['proxy_settings'].get('proxy_port')
        proxy_username = config['proxy_settings'].get('proxy_username')
        proxy_password = config['proxy_settings'].get('proxy_password')

        if proxy_host and proxy_port:
            proxy_str = f"{proxy_host}:{proxy_port}"

            if proxy_username and proxy_password:
                proxy_str = f"{proxy_username}:{proxy_password}@{proxy_str}"

            options.add_argument(f'--proxy-server=http://{proxy_str}')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(implicit_wait_time)
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {e}")
        raise

    logger.info("WebDriver setup completed")
    return driver
