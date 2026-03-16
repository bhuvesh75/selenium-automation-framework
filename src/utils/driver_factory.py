"""
@file        driver_factory.py
@description Factory that creates and configures Selenium WebDriver instances.
@purpose     Centralises browser creation so every test uses the same setup.
             Supports Chrome and Firefox with optional headless mode and
             remote WebDriver URL for Selenium Grid.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.config.config import BROWSER, HEADLESS, IMPLICIT_WAIT


def get_driver() -> webdriver.Remote:
    """
    Create and return a configured WebDriver instance.

    Reads BROWSER and HEADLESS from config. Supports an optional
    SELENIUM_REMOTE_URL environment variable for Selenium Grid.

    Returns:
        webdriver.Remote: A fully initialised WebDriver ready for test use.

    Raises:
        ValueError: If the browser name is not 'chrome' or 'firefox'.

    Example:
        driver = get_driver()
        driver.get('https://www.saucedemo.com')
    """
    # Check for a remote WebDriver URL (Selenium Grid / cloud provider)
    remote_url = os.getenv('SELENIUM_REMOTE_URL')

    if remote_url:
        # Use Remote WebDriver when a Grid URL is provided
        return _create_remote_driver(remote_url)

    # Select local browser based on config
    if BROWSER == 'chrome':
        return _create_chrome_driver(HEADLESS)
    elif BROWSER == 'firefox':
        return _create_firefox_driver(HEADLESS)
    else:
        raise ValueError(f"Unsupported browser: '{BROWSER}'. Use 'chrome' or 'firefox'.")


def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
    """
    Create a Chrome WebDriver with standard test options.

    Args:
        headless (bool): If True, Chrome runs without a visible window.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    options = ChromeOptions()

    if headless:
        # Use new headless mode (--headless=new) — more stable than legacy --headless
        options.add_argument('--headless=new')

    # Disable GPU acceleration — not needed for automated testing
    options.add_argument('--disable-gpu')
    # Required in Docker/CI containers where shared memory is limited
    options.add_argument('--no-sandbox')
    # Prevents crashes in resource-constrained environments
    options.add_argument('--disable-dev-shm-usage')
    # Standard HD viewport for consistent element visibility
    options.add_argument('--window-size=1280,720')
    # Disable browser notifications — they can block test interactions
    options.add_argument('--disable-notifications')

    # WHY: In CI, browser-actions/setup-chrome installs a matching chromedriver on
    # PATH and sets CHROMEDRIVER_PATH. Using it directly avoids webdriver-manager
    # picking the wrong file (e.g. THIRD_PARTY_NOTICES.chromedriver) on Linux runners.
    # Locally, webdriver-manager is used as a fallback so no manual install is needed.
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
    if chromedriver_path:
        # CI path: use the system chromedriver installed by setup-chrome action
        service = ChromeService(executable_path=chromedriver_path)
    else:
        # Local path: let webdriver-manager download and manage the driver
        service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Apply implicit wait — applies to all find_element calls globally
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver


def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
    """
    Create a Firefox (GeckoDriver) WebDriver.

    Args:
        headless (bool): If True, Firefox runs without a visible window.

    Returns:
        webdriver.Firefox: Configured Firefox WebDriver instance.
    """
    options = FirefoxOptions()

    if headless:
        # Firefox headless flag
        options.add_argument('--headless')

    # Automatically manage GeckoDriver installation
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver


def _create_remote_driver(remote_url: str) -> webdriver.Remote:
    """
    Create a Remote WebDriver for use with Selenium Grid or cloud providers.

    Args:
        remote_url (str): URL of the Selenium Grid hub (e.g., http://localhost:4444).

    Returns:
        webdriver.Remote: Configured remote WebDriver instance.
    """
    # Use Chrome capabilities for remote execution by default
    options = ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(command_executor=remote_url, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver
