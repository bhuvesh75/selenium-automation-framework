"""
@file        test_inventory.py
@description Functional tests for the Sauce Demo inventory (products) page.
@purpose     Validates product count, sorting behaviour, and product listing
             accuracy on the inventory page.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


@pytest.mark.functional
class TestInventory:
    """
    Inventory page functional test suite.

    Each test logs in first (setup within the test), then verifies
    product listing and sorting functionality.
    """

    def _login_and_get_inventory(self, driver) -> InventoryPage:
        """
        Helper: log in with standard_user and return an InventoryPage instance.

        Args:
            driver: The active WebDriver session.

        Returns:
            InventoryPage: Page object ready for inventory interactions.
        """
        # Log in to reach the inventory page
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login('standard_user', 'secret_sauce')
        # Return an InventoryPage instance bound to the same driver
        return InventoryPage(driver)

    def test_product_count_is_six(self, driver):
        """
        GIVEN the user is logged in
        WHEN  the inventory page loads
        THEN  exactly 6 products are displayed
        """
        # Arrange: log in and get inventory page
        inventory_page = self._login_and_get_inventory(driver)

        # Assert: saucedemo always shows 6 products
        assert inventory_page.get_product_count() == 6, \
            'Expected 6 products on the inventory page'

    def test_sort_a_to_z_first_item(self, driver):
        """
        GIVEN the user is on the inventory page
        WHEN  the sort dropdown is set to Name (A to Z)
        THEN  the first product is 'Sauce Labs Backpack'
        """
        # Arrange: log in and get inventory page
        inventory_page = self._login_and_get_inventory(driver)

        # Act: sort products alphabetically A to Z
        inventory_page.sort_by('az')

        # Assert: first product is Sauce Labs Backpack (alphabetically first)
        first_name = inventory_page.get_first_product_name()
        assert first_name == 'Sauce Labs Backpack', \
            f'Expected "Sauce Labs Backpack", got "{first_name}"'

    def test_sort_z_to_a_first_item(self, driver):
        """
        GIVEN the user is on the inventory page
        WHEN  the sort dropdown is set to Name (Z to A)
        THEN  the first product is 'Test.allTheThings() T-Shirt (Red)'
        """
        # Arrange: log in and get inventory page
        inventory_page = self._login_and_get_inventory(driver)

        # Act: sort products reverse alphabetically Z to A
        inventory_page.sort_by('za')

        # Assert: first product in Z-A order
        first_name = inventory_page.get_first_product_name()
        assert first_name == 'Test.allTheThings() T-Shirt (Red)', \
            f'Expected "Test.allTheThings() T-Shirt (Red)", got "{first_name}"'

    def test_sort_price_low_to_high_first_item(self, driver):
        """
        GIVEN the user is on the inventory page
        WHEN  the sort dropdown is set to Price (low to high)
        THEN  the first product is 'Sauce Labs Onesie' (cheapest at $7.99)
        """
        # Arrange: log in and get inventory page
        inventory_page = self._login_and_get_inventory(driver)

        # Act: sort products by price ascending
        inventory_page.sort_by('lohi')

        # Assert: cheapest product appears first
        first_name = inventory_page.get_first_product_name()
        assert first_name == 'Sauce Labs Onesie', \
            f'Expected "Sauce Labs Onesie" as cheapest, got "{first_name}"'
