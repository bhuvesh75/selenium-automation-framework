"""
@file        test_checkout.py
@description Functional tests for the Sauce Demo multi-step checkout flow.
@purpose     Validates the complete checkout journey: adding items, filling
             shipping info, verifying order summary, and confirming the order.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


@pytest.mark.functional
class TestCheckout:
    """
    Checkout functional test suite.

    Tests the full E2E checkout flow from adding items to order confirmation,
    plus individual step validations.
    """

    def _login_add_item_and_go_to_checkout(self, driver) -> CheckoutPage:
        """
        Helper: log in, add an item, navigate to cart, and click checkout.

        Args:
            driver: The active WebDriver session.

        Returns:
            CheckoutPage: Page object positioned at checkout step one.
        """
        # Log in with standard_user
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login('standard_user', 'secret_sauce')

        # Add a product to the cart
        inventory_page = InventoryPage(driver)
        inventory_page.add_product_to_cart('Sauce Labs Backpack')

        # Navigate to cart and proceed to checkout
        inventory_page.go_to_cart()
        cart_page = CartPage(driver)
        cart_page.click_checkout()

        # Return the checkout page object
        return CheckoutPage(driver)

    def test_full_checkout_flow_displays_confirmation(self, driver):
        """
        GIVEN the user has an item in the cart and is on checkout step one
        WHEN  shipping info is filled, continue is clicked, and finish is clicked
        THEN  the confirmation page displays 'Thank you for your order!'
        """
        # Arrange: get to checkout step one with an item
        checkout_page = self._login_add_item_and_go_to_checkout(driver)

        # Act: fill shipping info and complete checkout
        checkout_page.fill_shipping_info('John', 'Doe', '12345')
        checkout_page.click_continue()
        checkout_page.click_finish()

        # Assert: confirmation message is displayed
        message = checkout_page.get_thank_you_message()
        assert 'THANK YOU FOR YOUR ORDER' in message.upper(), \
            f'Expected thank-you message, got: {message}'

    def test_order_total_contains_dollar_sign(self, driver):
        """
        GIVEN the user has completed shipping info on checkout step one
        WHEN  the user advances to the order summary on step two
        THEN  the order total contains a '$' symbol
        """
        # Arrange: get to checkout step one
        checkout_page = self._login_add_item_and_go_to_checkout(driver)

        # Act: fill shipping info and advance to summary
        checkout_page.fill_shipping_info('John', 'Doe', '12345')
        checkout_page.click_continue()

        # Assert: total includes dollar sign
        total = checkout_page.get_order_total()
        assert '$' in total, \
            f'Expected "$" in order total, got: {total}'

    def test_step_navigation_reaches_step_two(self, driver):
        """
        GIVEN the user is on checkout step one with shipping info filled
        WHEN  the Continue button is clicked
        THEN  the URL contains 'checkout-step-two'
        """
        # Arrange: get to checkout step one
        checkout_page = self._login_add_item_and_go_to_checkout(driver)

        # Act: fill info and continue
        checkout_page.fill_shipping_info('John', 'Doe', '12345')
        checkout_page.click_continue()

        # Assert: URL indicates step two
        assert checkout_page.is_on_step_two(), \
            'Expected to be on checkout step two after filling info'
