"""
@file        base_page.py
@description Abstract base class for all Page Object classes.
@purpose     Centralises shared Selenium interactions (click, type, getText)
             so page classes contain only their own selectors and high-level actions.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from src.utils.wait_helper import WaitHelper
from src.config.config import BASE_URL


class BasePage:
    """
    Base class for all Page Objects.

    Provides shared low-level Selenium actions that every page needs:
    navigation, clicks, text input, and element queries. Page-specific
    classes extend this and add their own selectors and business-logic methods.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialise BasePage with the active WebDriver and a WaitHelper.

        Args:
            driver (WebDriver): The active Selenium WebDriver session.
        """
        # Store the driver for use in all page methods
        self.driver = driver
        # WaitHelper wraps explicit waits with descriptive error messages
        self.wait = WaitHelper(driver)

    def navigate_to(self, path: str = '') -> None:
        """
        Navigate to a path relative to the configured BASE_URL.

        Args:
            path (str): URL path to append (e.g., '/inventory.html').

        Example:
            self.navigate_to('/inventory.html')
        """
        # Strip trailing slash from base and leading slash from path to avoid double slashes
        url = BASE_URL.rstrip('/') + '/' + path.lstrip('/')
        self.driver.get(url)

    def click(self, locator: tuple) -> None:
        """
        Wait for element to be clickable and click it.

        Args:
            locator (tuple): Selenium By locator, e.g. (By.ID, 'login-button').

        Example:
            self.click((By.ID, 'login-button'))
        """
        # Wait until the element is both visible and enabled before clicking
        element = self.wait.wait_for_element_clickable(locator)
        element.click()

    def type(self, locator: tuple, text: str) -> None:
        """
        Clear an input field and type the given text.

        Args:
            locator (tuple): Selenium By locator for the input field.
            text    (str):   Text to enter into the field.

        Example:
            self.type((By.ID, 'user-name'), 'standard_user')
        """
        # Wait for the field to be visible before interacting
        element = self.wait.wait_for_element_visible(locator)
        # Clear any pre-existing value before typing the new one
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """
        Return the visible text content of an element.

        Args:
            locator (tuple): Selenium By locator.

        Returns:
            str: Stripped text content of the element.

        Example:
            message = self.get_text((By.CLASS_NAME, 'error-message'))
        """
        element = self.wait.wait_for_element_visible(locator)
        # Strip leading/trailing whitespace for reliable assertions
        return element.text.strip()

    def is_displayed(self, locator: tuple) -> bool:
        """
        Check whether an element is currently visible without waiting.

        Args:
            locator (tuple): Selenium By locator.

        Returns:
            bool: True if element exists and is visible, False otherwise.

        Example:
            visible = self.is_displayed((By.ID, 'shopping_cart_badge'))
        """
        try:
            # find_elements returns an empty list (not an exception) if no match
            elements = self.driver.find_elements(*locator)
            return len(elements) > 0 and elements[0].is_displayed()
        except Exception:
            # Catch any driver-level exceptions and treat as not displayed
            return False

    def get_current_url(self) -> str:
        """
        Return the browser's current URL.

        Returns:
            str: The full current URL.

        Example:
            url = self.get_current_url()
            assert '/inventory.html' in url
        """
        return self.driver.current_url

    def get_title(self) -> str:
        """
        Return the browser tab title.

        Returns:
            str: The document title string.

        Example:
            assert self.get_title() == 'Swag Labs'
        """
        return self.driver.title
