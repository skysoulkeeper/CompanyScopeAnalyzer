# modules/webdriver_setup.py
import json
from utils.logger import logger
import undetected_chromedriver as uc
from typing import Dict


# Define a function to set up the WebDriver
def setup_webdriver(config: Dict[str, any]) -> uc.Chrome:
    # Extract proxy and WebDriver configuration from the provided 'config' dictionary
    proxy_settings = config.get('proxy_settings', {})
    webdriver_config = config.get('webdriver', {})

    # Log the proxy and WebDriver configuration before setting up the WebDriver
    logger.info("Proxy Settings: {}", json.dumps(proxy_settings))
    logger.info("WebDriver Configuration: {}", json.dumps(webdriver_config))

    # Configure WebDriver options
    options = uc.ChromeOptions()
    #    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-login-animations")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-cookies")
    options.add_argument("--disable-gpu")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("accept-language=en-US,en;q=0.9")

    # Check if 'webdriver' key exists in the configuration
    if 'webdriver' not in config:
        raise KeyError("WebDriver configuration not found in config.")

    # Retrieve user agent and implicit wait time from WebDriver configuration
    webdriver_config = config['webdriver']
    user_agent = webdriver_config.get('user_agent')
    implicit_wait_time = webdriver_config.get('implicit_wait_time')
    headless_mode = webdriver_config.get('headless', False)

    # Check if user agent and implicit wait time are provided
    if user_agent is None or implicit_wait_time is None:
        raise KeyError("Missing required WebDriver configuration parameters.")

    # Add user agent to WebDriver options
    options.add_argument("--user-agent=" + user_agent)

    # Retrieve headless mode setting from WebDriver configuration
    if headless_mode:
        options.add_argument("--headless")

    # Proxy Configuration
    if 'proxy_settings' in config and config['proxy_settings'].get('proxy_enabled'):
        proxy_host = config['proxy_settings'].get('proxy_host')
        proxy_port = config['proxy_settings'].get('proxy_port')
        proxy_username = config['proxy_settings'].get('proxy_username')
        proxy_password = config['proxy_settings'].get('proxy_password')

        # Construct the proxy string
        if proxy_host and proxy_port:
            proxy_str = f"{proxy_host}:{proxy_port}"

            if proxy_username and proxy_password:
                proxy_str = f"{proxy_username}:{proxy_password}@{proxy_str}"

            options.add_argument(f'--proxy-server=http://{proxy_str}')

    try:
        # Set up the WebDriver using ChromeDriverManager
        driver = uc.Chrome(options=options)
        driver.implicitly_wait(implicit_wait_time)
    except Exception as e:
        # Handle any exceptions that may occur during WebDriver setup
        logger.error(f"Error setting up WebDriver: {e}")
        raise

    # Log a message to indicate that WebDriver setup is completed
    logger.info("WebDriver setup completed")

    # Return the configured WebDriver instance
    return driver
