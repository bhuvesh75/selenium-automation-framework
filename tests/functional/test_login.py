"""
@file        test_login.py
@description Functional tests for the Sauce Demo login feature.
@purpose     Validates login behaviour for valid credentials, invalid credentials,
             locked-out accounts, and missing field scenarios using data-driven
             parameterisation.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.pages.login_page import LoginPage


@pytest.mark.functional
class TestLogin:
    """
    Login functional test suite.

    Covers positive login flows (data-driven), negative login flows
    (wrong password, locked user), and validation errors (empty fields).
    """

    @pytest.mark.parametrize('username, password', [
        ('standard_user', 'secret_sauce'),
        ('performance_glitch_user', 'secret_sauce'),
    ])
    def test_valid_login_should_succeed(self, driver, username, password):
        """
        GIVEN valid credentials for a supported user type
        WHEN  the user submits the login form
        THEN  the browser navigates to the inventory page
        """
        # Arrange: navigate to login
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: perform login with parameterised credentials
        login_page.login(username, password)

        # Assert: successfully reached inventory page
        assert '/inventory.html' in driver.current_url, \
            f'Login failed for user: {username}'

    def test_invalid_password_should_show_error(self, driver):
        """
        GIVEN a valid username but an incorrect password
        WHEN  the user submits the login form
        THEN  an error message containing 'Username and password do not match' is displayed
        """
        # Arrange: navigate to login
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: attempt login with wrong password
        login_page.login('standard_user', 'wrong_password')

        # Assert: error message indicates credential mismatch
        error = login_page.get_error_message()
        assert 'Username and password do not match' in error, \
            f'Expected credential mismatch error, got: {error}'

    def test_locked_out_user_should_show_locked_error(self, driver):
        """
        GIVEN the locked_out_user account
        WHEN  the user submits correct credentials
        THEN  an error message containing 'locked out' is displayed
        """
        # Arrange: navigate to login
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: attempt login with the locked-out user
        login_page.login('locked_out_user', 'secret_sauce')

        # Assert: error mentions locked out
        error = login_page.get_error_message()
        assert 'locked out' in error.lower(), \
            f'Expected locked-out error, got: {error}'

    def test_empty_username_should_show_required_error(self, driver):
        """
        GIVEN an empty username field
        WHEN  the user submits the login form with only a password
        THEN  an error message containing 'Username is required' is displayed
        """
        # Arrange: navigate to login
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: submit with empty username but a password
        login_page.enter_password('secret_sauce')
        login_page.click_login()

        # Assert: validation error for missing username
        error = login_page.get_error_message()
        assert 'Username is required' in error, \
            f'Expected username required error, got: {error}'

    def test_empty_password_should_show_required_error(self, driver):
        """
        GIVEN an empty password field
        WHEN  the user submits the login form with only a username
        THEN  an error message containing 'Password is required' is displayed
        """
        # Arrange: navigate to login
        login_page = LoginPage(driver)
        login_page.navigate()

        # Act: submit with username but empty password
        login_page.enter_username('standard_user')
        login_page.click_login()

        # Assert: validation error for missing password
        error = login_page.get_error_message()
        assert 'Password is required' in error, \
            f'Expected password required error, got: {error}'
