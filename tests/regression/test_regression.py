"""
@file        test_regression.py
@description Full end-to-end regression test covering the entire happy path.
@purpose     Runs the complete user journey in one sequential test: login,
             browse products, sort, add to cart, verify cart, checkout,
             fill shipping info, verify summary, complete order, and confirm.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


@pytest.mark.regression
class TestRegression:
    """
    Regression test suite — full user journey through the application.

    This single test covers the entire happy path in sequential steps
    with assertions at every critical transition point.
    """

    def test_complete_user_journey(self, driver):
        """
        GIVEN the application is deployed and accessible
        WHEN  a user logs in, browses products, sorts them, adds items to the cart,
              proceeds through checkout with shipping info, and completes the order
        THEN  every step succeeds and the order confirmation is displayed

        This test validates the entire happy path in one sequential flow:
        1. Login with valid credentials
        2. Verify inventory page loads with correct product count
        3. Sort products and verify sort order
        4. Add a product to the cart
        5. Verify cart badge updates
        6. Navigate to cart and verify contents
        7. Proceed to checkout step one
        8. Fill shipping information
        9. Advance to step two and verify order summary
        10. Complete the order and verify confirmation
        """
        # ─────────────────────────────────────────────────────────
        # STEP 1: Login
        # ─────────────────────────────────────────────────────────
        login_page = LoginPage(driver)
        login_page.navigate()

        # Verify the login page rendered correctly
        assert login_page.is_on_login_page(), 'Should start on the login page'

        # Log in with valid credentials
        login_page.login('standard_user', 'secret_sauce')

        # ─────────────────────────────────────────────────────────
        # STEP 2: Verify inventory page
        # ─────────────────────────────────────────────────────────
        inventory_page = InventoryPage(driver)

        # Confirm we reached the inventory page
        assert inventory_page.is_on_inventory_page(), \
            'Should be on inventory page after login'

        # Verify all 6 products are displayed
        assert inventory_page.get_product_count() == 6, \
            'Inventory should display 6 products'

        # ─────────────────────────────────────────────────────────
        # STEP 3: Sort products
        # ─────────────────────────────────────────────────────────

        # Sort A to Z and verify
        inventory_page.sort_by('az')
        assert inventory_page.get_first_product_name() == 'Sauce Labs Backpack', \
            'First product in A-Z sort should be Sauce Labs Backpack'

        # Sort Z to A and verify
        inventory_page.sort_by('za')
        assert inventory_page.get_first_product_name() == 'Test.allTheThings() T-Shirt (Red)', \
            'First product in Z-A sort should be Test.allTheThings() T-Shirt (Red)'

        # ─────────────────────────────────────────────────────────
        # STEP 4: Add product to cart
        # ─────────────────────────────────────────────────────────

        # Sort back to A-Z for consistent product selection
        inventory_page.sort_by('az')

        # Add Sauce Labs Backpack to the cart
        inventory_page.add_product_to_cart('Sauce Labs Backpack')

        # ─────────────────────────────────────────────────────────
        # STEP 5: Verify cart badge
        # ─────────────────────────────────────────────────────────

        # Cart badge should show 1 after adding one item
        badge_count = inventory_page.get_cart_badge_count()
        assert badge_count == 1, \
            f'Cart badge should show 1, got {badge_count}'

        # ─────────────────────────────────────────────────────────
        # STEP 6: Navigate to cart and verify contents
        # ─────────────────────────────────────────────────────────

        # Go to the cart page
        inventory_page.go_to_cart()
        cart_page = CartPage(driver)

        # Verify we are on the cart page
        assert cart_page.is_on_cart_page(), 'Should be on the cart page'

        # Verify the cart has exactly 1 item
        assert cart_page.get_item_count() == 1, \
            'Cart should contain 1 item'

        # ─────────────────────────────────────────────────────────
        # STEP 7: Proceed to checkout
        # ─────────────────────────────────────────────────────────

        # Click checkout to start the checkout flow
        cart_page.click_checkout()
        checkout_page = CheckoutPage(driver)

        # Verify we are on checkout step one
        assert checkout_page.is_on_step_one(), \
            'Should be on checkout step one'

        # ─────────────────────────────────────────────────────────
        # STEP 8: Fill shipping information
        # ─────────────────────────────────────────────────────────

        # Enter customer shipping details
        checkout_page.fill_shipping_info('John', 'Doe', '12345')

        # Click Continue to advance to step two
        checkout_page.click_continue()

        # ─────────────────────────────────────────────────────────
        # STEP 9: Verify order summary
        # ─────────────────────────────────────────────────────────

        # Confirm we are on step two (order summary)
        assert checkout_page.is_on_step_two(), \
            'Should be on checkout step two'

        # Verify the order total contains a dollar sign
        total = checkout_page.get_order_total()
        assert '$' in total, \
            f'Order total should contain "$", got: {total}'

        # Verify the correct item name appears in the summary
        item_name = checkout_page.get_summary_item_name()
        assert item_name == 'Sauce Labs Backpack', \
            f'Summary should show "Sauce Labs Backpack", got: {item_name}'

        # ─────────────────────────────────────────────────────────
        # STEP 10: Complete order and verify confirmation
        # ─────────────────────────────────────────────────────────

        # Click Finish to complete the order
        checkout_page.click_finish()

        # Verify we are on the confirmation page
        assert checkout_page.is_on_confirmation(), \
            'Should be on the order confirmation page'

        # Verify the thank-you message is displayed
        message = checkout_page.get_thank_you_message()
        assert 'THANK YOU FOR YOUR ORDER' in message.upper(), \
            f'Expected thank-you message, got: {message}'
