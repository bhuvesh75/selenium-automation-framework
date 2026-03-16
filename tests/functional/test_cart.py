"""
@file        test_cart.py
@description Functional tests for the Sauce Demo shopping cart.
@purpose     Validates add-to-cart, remove-from-cart, cart badge count,
             and navigation between cart and inventory pages.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage


@pytest.mark.functional
class TestCart:
    """
    Cart functional test suite.

    Tests cart interactions: adding products, verifying badge counts,
    removing products, and navigating between cart and inventory.
    """

    def _login(self, driver) -> InventoryPage:
        """
        Helper: log in with standard_user and return an InventoryPage instance.

        Args:
            driver: The active WebDriver session.

        Returns:
            InventoryPage: Page object for inventory interactions.
        """
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login('standard_user', 'secret_sauce')
        return InventoryPage(driver)

    def test_add_two_products_shows_badge_count_two(self, driver):
        """
        GIVEN the user is logged in on the inventory page
        WHEN  two different products are added to the cart
        THEN  the cart badge displays '2'
        """
        # Arrange: log in
        inventory_page = self._login(driver)

        # Act: add two products to the cart
        inventory_page.add_product_to_cart('Sauce Labs Backpack')
        inventory_page.add_product_to_cart('Sauce Labs Bike Light')

        # Assert: cart badge shows 2
        badge_count = inventory_page.get_cart_badge_count()
        assert badge_count == 2, \
            f'Expected cart badge count 2, got {badge_count}'

    def test_remove_one_product_shows_badge_count_one(self, driver):
        """
        GIVEN the user has two products in the cart
        WHEN  one product is removed from the cart page
        THEN  the cart badge displays '1'
        """
        # Arrange: log in and add two products
        inventory_page = self._login(driver)
        inventory_page.add_product_to_cart('Sauce Labs Backpack')
        inventory_page.add_product_to_cart('Sauce Labs Bike Light')

        # Act: go to cart and remove one product
        inventory_page.go_to_cart()
        cart_page = CartPage(driver)
        cart_page.remove_item('Sauce Labs Backpack')

        # Assert: one item remains in the cart
        assert cart_page.get_item_count() == 1, \
            'Expected 1 item remaining in cart after removal'

    def test_continue_shopping_returns_to_inventory(self, driver):
        """
        GIVEN the user is on the cart page
        WHEN  the Continue Shopping button is clicked
        THEN  the browser navigates back to /inventory.html
        """
        # Arrange: log in and go to cart
        inventory_page = self._login(driver)
        inventory_page.go_to_cart()
        cart_page = CartPage(driver)

        # Act: click Continue Shopping
        cart_page.click_continue_shopping()

        # Assert: URL is the inventory page
        assert '/inventory.html' in driver.current_url, \
            'Expected to return to inventory page after Continue Shopping'
