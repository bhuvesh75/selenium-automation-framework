"""
@file        login_page.py
@description Page Object for the Sauce Demo login screen.
@purpose     Encapsulates all selectors and actions for login flows
             so tests never reference raw CSS selectors directly.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

# ─────────────────────────────────────────────────────────────
# SECTION: Element Locators
# ─────────────────────────────────────────────────────────────

# Username input field — ID attribute defined in saucedemo HTML
USERNAME_FIELD = (By.ID, 'user-name')

# Password input field
PASSWORD_FIELD = (By.ID, 'password')

# Login submit button
LOGIN_BUTTON = (By.ID, 'login-button')

# Error message container — appears for failed login attempts
ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')


class LoginPage(BasePage):
    """
    Page Object for https://www.saucedemo.com (login screen).

    Provides high-level actions (login, getErrorMessage) so test files
    read like behaviour specifications rather than Selenium instructions.
    """

    def navigate(self) -> None:
        """
        Navigate directly to the login page (root URL).

        Example:
            login_page.navigate()
        """
        # Navigate to the root — saucedemo shows the login form at /
        self.navigate_to('/')

    def enter_username(self, username: str) -> None:
        """
        Type the username into the username input field.

        Args:
            username (str): The username to enter.

        Example:
            login_page.enter_username('standard_user')
        """
        self.type(USERNAME_FIELD, username)

    def enter_password(self, password: str) -> None:
        """
        Type the password into the password input field.

        Args:
            password (str): The password to enter.
        """
        self.type(PASSWORD_FIELD, password)

    def click_login(self) -> None:
        """
        Click the Login button to submit the form.
        """
        self.click(LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        Perform a complete login: enter credentials and click Login.

        Args:
            username (str): The username to log in with.
            password (str): The password to log in with.

        Example:
            login_page.login('standard_user', 'secret_sauce')
        """
        # Fill username field
        self.enter_username(username)
        # Fill password field
        self.enter_password(password)
        # Submit the form
        self.click_login()

    def get_error_message(self) -> str:
        """
        Return the text of the error message shown after a failed login.

        Returns:
            str: The error message text.

        Example:
            assert 'Username and password do not match' in login_page.get_error_message()
        """
        # Wait for the error element to appear and return its text
        return self.get_text(ERROR_MESSAGE)

    def is_on_login_page(self) -> bool:
        """
        Check whether the browser is currently on the login page.

        Returns:
            bool: True if the URL does not contain '/inventory'.
        """
        # Login page is at the root — no path fragment to check
        return '/inventory' not in self.get_current_url()
