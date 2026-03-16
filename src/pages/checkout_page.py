"""
@file        checkout_page.py
@description Page Object for the Sauce Demo multi-step checkout flow.
@purpose     Encapsulates selectors and actions for checkout step one (shipping info),
             step two (order summary), and the order confirmation page.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


# ─────────────────────────────────────────────────────────────
# SECTION: Step One Locators (Shipping Information)
# ─────────────────────────────────────────────────────────────

# First name input field on checkout step one
FIRST_NAME_FIELD = (By.ID, 'first-name')

# Last name input field on checkout step one
LAST_NAME_FIELD = (By.ID, 'last-name')

# Zip/postal code input field on checkout step one
ZIP_CODE_FIELD = (By.ID, 'postal-code')

# Continue button — proceeds from step one to step two
CONTINUE_BUTTON = (By.ID, 'continue')

# ─────────────────────────────────────────────────────────────
# SECTION: Step Two Locators (Order Summary)
# ─────────────────────────────────────────────────────────────

# Order summary total label — shows the total price including tax
SUMMARY_TOTAL = (By.CLASS_NAME, 'summary_total_label')

# Item name on the summary page — product being purchased
SUMMARY_ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')

# Finish button — completes the order
FINISH_BUTTON = (By.ID, 'finish')

# ─────────────────────────────────────────────────────────────
# SECTION: Confirmation Page Locators
# ─────────────────────────────────────────────────────────────

# Thank you header — displayed after successful order completion
THANK_YOU_HEADER = (By.CLASS_NAME, 'complete-header')

# Back Home button — returns to the inventory page after order
BACK_HOME_BUTTON = (By.ID, 'back-to-products')


class CheckoutPage(BasePage):
    """
    Page Object for the Sauce Demo checkout flow.

    Covers three checkout stages:
    1. Step One — enter shipping information (first name, last name, zip code)
    2. Step Two — review order summary and total
    3. Confirmation — verify the order was placed successfully

    Each stage has its own URL path, enabling URL-based page verification.
    """

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str) -> None:
        """
        Fill in all shipping information fields on checkout step one.

        Args:
            first_name (str): Customer's first name.
            last_name  (str): Customer's last name.
            zip_code   (str): Shipping zip/postal code.

        Example:
            checkout_page.fill_shipping_info('John', 'Doe', '12345')
        """
        for locator, value in [
            (FIRST_NAME_FIELD, first_name),
            (LAST_NAME_FIELD, last_name),
            (ZIP_CODE_FIELD, zip_code),
        ]:
            element = self.wait.wait_for_element_visible(locator)
            # WHY: React controlled inputs require the native value setter plus an
            # 'input' event to update React's internal state. element.clear() +
            # send_keys() fires keyboard events which should work, but in headless
            # Chrome the synthetic event chain sometimes fails to update React state,
            # leaving fields appearing empty to saucedemo's form validation — which
            # then blocks the Continue button from navigating to step two.
            # Using the native HTMLInputElement value setter + dispatchEvent('input')
            # is the canonical approach for programmatically setting React controlled
            # input values and is guaranteed to trigger React's onChange handler.
            self.driver.execute_script("""
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                setter.call(arguments[0], arguments[1]);
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, element, value)

    def click_continue(self) -> None:
        """
        Click the Continue button to proceed from step one to step two.

        Example:
            checkout_page.click_continue()
        """
        # WHY: JS click bypasses potential React-render interception that causes
        # standard .click() to silently fail without navigating to step two.
        continue_btn = self.wait.wait_for_element_visible(CONTINUE_BUTTON)
        self.driver.execute_script("arguments[0].click();", continue_btn)
        # Wait for URL to confirm navigation to step two is complete
        self.wait.wait_for_url_contains('checkout-step-two')

    def click_finish(self) -> None:
        """
        Click the Finish button on step two to complete the order.

        Example:
            checkout_page.click_finish()
        """
        # WHY: JS click ensures navigation even when React is mid-update
        finish_btn = self.wait.wait_for_element_visible(FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", finish_btn)
        # Wait for URL to confirm order completion page is loaded
        self.wait.wait_for_url_contains('checkout-complete')

    def get_order_total(self) -> str:
        """
        Return the order total string from the summary page.

        Returns:
            str: The total price text (e.g., 'Total: $32.39').

        Example:
            total = checkout_page.get_order_total()
            assert '$' in total
        """
        # Read the summary total label text
        return self.get_text(SUMMARY_TOTAL)

    def get_summary_item_name(self) -> str:
        """
        Return the product name displayed on the order summary page.

        Returns:
            str: The item name as shown in the order summary.

        Example:
            name = checkout_page.get_summary_item_name()
            assert name == 'Sauce Labs Backpack'
        """
        return self.get_text(SUMMARY_ITEM_NAME)

    def is_on_step_one(self) -> bool:
        """
        Check whether the browser is on checkout step one.

        Returns:
            bool: True if the URL contains 'checkout-step-one'.

        Example:
            assert checkout_page.is_on_step_one()
        """
        return 'checkout-step-one' in self.get_current_url()

    def is_on_step_two(self) -> bool:
        """
        Check whether the browser is on checkout step two (order summary).

        Returns:
            bool: True if the URL contains 'checkout-step-two'.

        Example:
            assert checkout_page.is_on_step_two()
        """
        return 'checkout-step-two' in self.get_current_url()

    def is_on_confirmation(self) -> bool:
        """
        Check whether the browser is on the order confirmation page.

        Returns:
            bool: True if the URL contains 'checkout-complete'.

        Example:
            assert checkout_page.is_on_confirmation()
        """
        return 'checkout-complete' in self.get_current_url()

    def get_thank_you_message(self) -> str:
        """
        Return the thank-you message displayed after order completion.

        Returns:
            str: The confirmation header text (e.g., 'Thank you for your order!').

        Example:
            message = checkout_page.get_thank_you_message()
            assert 'THANK YOU' in message.upper()
        """
        # Wait for and return the complete-header text
        return self.get_text(THANK_YOU_HEADER)

    def click_back_home(self) -> None:
        """
        Click the Back Home button to return to the inventory page.

        Example:
            checkout_page.click_back_home()
        """
        # Navigate back to inventory after order confirmation
        self.click(BACK_HOME_BUTTON)
