"""
@file        test_smoke.py
@description Quick sanity checks to verify the application is reachable.
@purpose     Smoke suite runs before full functional tests to confirm the
             application is up and basic navigation works.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from selenium.webdriver.common.by import By
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


@pytest.mark.smoke
class TestSmoke:
    """
    Smoke test suite — fast sanity checks that the application is alive.

    These tests run first in CI to catch deployment failures early
    before investing time in the full functional suite.
    """

    def test_login_page_loads(self, driver):
        """
        GIVEN the application is deployed
        WHEN  the user navigates to the base URL
        THEN  the login form is visible with username and password fields
        """
        # Arrange: navigate to the application
        login_page = LoginPage(driver)
        login_page.navigate()

        # Assert: login form elements are present
        assert login_page.is_displayed((By.ID, 'user-name')), 'Username field not visible'
        assert login_page.is_displayed((By.ID, 'password')), 'Password field not visible'
        assert login_page.is_displayed((By.ID, 'login-button')), 'Login button not visible'

    def test_valid_login_reaches_inventory(self, driver):
        """
        GIVEN valid credentials (standard_user / secret_sauce)
        WHEN  the user submits the login form
        THEN  the browser navigates to /inventory.html
        """
        # Arrange: navigate to login page
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: log in with valid credentials
        login_page.login('standard_user', 'secret_sauce')

        # Assert: redirected to the inventory page
        assert '/inventory.html' in driver.current_url

    def test_page_title(self, driver):
        """
        GIVEN the application is deployed
        WHEN  the user navigates to the base URL
        THEN  the page title is 'Swag Labs'
        """
        # Arrange: navigate to the application
        login_page = LoginPage(driver)
        login_page.navigate()

        # Assert: page title matches expected value
        assert login_page.get_title() == 'Swag Labs'
