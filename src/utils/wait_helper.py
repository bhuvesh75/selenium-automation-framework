"""
@file        wait_helper.py
@description Explicit and fluent wait wrappers for Selenium WebDriver.
@purpose     Provides descriptive wait methods that produce clear timeout
             messages, replacing raw WebDriverWait calls in page classes.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.config.config import EXPLICIT_WAIT


class WaitHelper:
    """
    Encapsulates Selenium explicit waits with human-readable timeout messages.

    All methods accept a By locator tuple and an optional timeout in seconds.
    When a wait expires, the TimeoutException message will include the locator
    so developers can immediately identify which element caused the failure.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialise WaitHelper with the active WebDriver.

        Args:
            driver (WebDriver): The active Selenium WebDriver session.
        """
        # Store driver reference for use in all wait methods
        self.driver = driver

    def wait_for_element_visible(self, locator: tuple, seconds: int = EXPLICIT_WAIT) -> WebElement:
        """
        Wait until the element identified by locator is visible in the DOM.

        Args:
            locator (tuple): Selenium By locator, e.g. (By.ID, 'user-name').
            seconds (int):   Maximum seconds to wait. Defaults to EXPLICIT_WAIT.

        Returns:
            WebElement: The visible element.

        Raises:
            TimeoutException: If element is not visible within the timeout.

        Example:
            element = wait.wait_for_element_visible((By.ID, 'user-name'))
        """
        # Use WebDriverWait with visibility_of_element_located condition
        return WebDriverWait(self.driver, seconds).until(
            EC.visibility_of_element_located(locator),
            message=f'Element not visible after {seconds}s: {locator}'
        )

    def wait_for_element_clickable(self, locator: tuple, seconds: int = EXPLICIT_WAIT) -> WebElement:
        """
        Wait until the element is visible AND enabled (i.e., clickable).

        Args:
            locator (tuple): Selenium By locator.
            seconds (int):   Maximum seconds to wait.

        Returns:
            WebElement: The clickable element.

        Raises:
            TimeoutException: If element is not clickable within the timeout.

        Example:
            button = wait.wait_for_element_clickable((By.ID, 'login-button'))
        """
        return WebDriverWait(self.driver, seconds).until(
            EC.element_to_be_clickable(locator),
            message=f'Element not clickable after {seconds}s: {locator}'
        )

    def wait_for_text_present(self, locator: tuple, text: str, seconds: int = EXPLICIT_WAIT) -> bool:
        """
        Wait until the element's text contains the expected string.

        Args:
            locator (tuple): Selenium By locator.
            text    (str):   The text expected to appear in the element.
            seconds (int):   Maximum seconds to wait.

        Returns:
            bool: True when the text is present.

        Raises:
            TimeoutException: If text does not appear within the timeout.

        Example:
            wait.wait_for_text_present((By.CLASS_NAME, 'error'), 'invalid')
        """
        return WebDriverWait(self.driver, seconds).until(
            EC.text_to_be_present_in_element(locator, text),
            message=f'Text "{text}" not found in {locator} after {seconds}s'
        )

    def wait_for_url_contains(self, url_fragment: str, seconds: int = EXPLICIT_WAIT) -> bool:
        """
        Wait until the current URL contains a given substring.

        Args:
            url_fragment (str): Expected substring in the URL.
            seconds      (int): Maximum seconds to wait.

        Returns:
            bool: True when URL contains the fragment.

        Example:
            wait.wait_for_url_contains('/inventory.html')
        """
        return WebDriverWait(self.driver, seconds).until(
            EC.url_contains(url_fragment),
            message=f'URL did not contain "{url_fragment}" after {seconds}s'
        )
