"""
@file        cart_page.py
@description Page Object for the Sauce Demo shopping cart page.
@purpose     Encapsulates all selectors and actions for the cart page so tests
             interact through clean methods rather than raw Selenium locators.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.base_page import BasePage
from src.config.config import IMPLICIT_WAIT, EXPLICIT_WAIT

# ─────────────────────────────────────────────────────────────
# SECTION: Element Locators
# ─────────────────────────────────────────────────────────────

# Individual cart item containers — each added product appears as one of these
CART_ITEMS = (By.CLASS_NAME, 'cart_item')

# Product name within each cart item
CART_ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')

# Checkout button — navigates to checkout step one
CHECKOUT_BUTTON = (By.ID, 'checkout')

# Continue Shopping button — navigates back to inventory
CONTINUE_SHOPPING_BUTTON = (By.ID, 'continue-shopping')

# Remove buttons within cart items — each item has one
REMOVE_BUTTON = (By.CSS_SELECTOR, 'button.cart_button')


class CartPage(BasePage):
    """
    Page Object for https://www.saucedemo.com/cart.html.

    Provides methods to inspect cart contents, remove items,
    and navigate to checkout or back to inventory.
    """

    def get_item_count(self) -> int:
        """
        Return the number of items currently in the cart.

        Returns:
            int: Count of cart item elements on the page.

        Example:
            assert cart_page.get_item_count() == 2
        """
        # Find all cart item containers and return the count
        items = self.driver.find_elements(*CART_ITEMS)
        return len(items)

    def remove_item(self, product_name: str) -> None:
        """
        Remove a specific product from the cart by its name.

        Finds the cart item whose name matches the given product_name,
        then clicks the Remove button within that item's container.

        Args:
            product_name (str): Exact name of the product to remove.

        Raises:
            ValueError: If no cart item with the given name is found.

        Example:
            cart_page.remove_item('Sauce Labs Backpack')
        """
        # Wait for at least one cart item to be visible before iterating
        # WHY: find_elements returns an empty list immediately if called before DOM is ready
        self.wait.wait_for_element_visible(CART_ITEMS)
        # Find all cart item containers
        items = self.driver.find_elements(*CART_ITEMS)

        for item in items:
            # Check if this item's name matches
            name_element = item.find_element(*CART_ITEM_NAME)
            if name_element.text.strip() == product_name:
                # WHY: saucedemo uses data-test="remove-*" on remove buttons — more reliable
                remove_btn = item.find_element(By.CSS_SELECTOR, 'button[data-test^="remove"]')
                # WHY: JS click bypasses React's event interception during DOM updates.
                # Standard .click() can be silently absorbed when React is mid-render
                # (e.g., immediately after navigating to the cart page), causing the
                # remove action to not fire and the item count to stay at 2.
                self.driver.execute_script("arguments[0].click();", remove_btn)

                # WHY: React removes the cart item from the DOM asynchronously.
                # Without waiting for the item to disappear, get_item_count()
                # may read the DOM before React's update and return the old count.
                # Disable implicit wait during this explicit poll to avoid the
                # known antipattern of mixing implicit and explicit waits.
                self.driver.implicitly_wait(0)
                try:
                    # WHY timeout=EXPLICIT_WAIT (15s) not 10s: CI runners are
                    # resource-constrained and React's async DOM removal can take
                    # up to ~12s under load. 15s matches EXPLICIT_WAIT for
                    # project-wide consistency and eliminates flaky timeouts.
                    WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                        lambda d: not any(
                            el.find_elements(*CART_ITEM_NAME) and
                            el.find_elements(*CART_ITEM_NAME)[0].text.strip() == product_name
                            for el in d.find_elements(*CART_ITEMS)
                        )
                    )
                finally:
                    self.driver.implicitly_wait(IMPLICIT_WAIT)
                return

        # No matching product found in the cart
        raise ValueError(f"Product '{product_name}' not found in the cart.")

    def click_checkout(self) -> None:
        """
        Click the Checkout button to proceed to checkout step one.

        Example:
            cart_page.click_checkout()
        """
        # WHY: Use JavaScript click for checkout navigation. Standard WebDriver
        # .click() can be intercepted when React is still processing a prior
        # state update (e.g. after add-to-cart or remove-item). JS click
        # dispatches directly to the DOM element, bypassing any overlay.
        checkout_btn = self.wait.wait_for_element_visible(CHECKOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", checkout_btn)
        # WHY: wait for URL change confirms checkout step-one page has loaded
        # before tests attempt to fill form fields — prevents TimeoutException
        self.wait.wait_for_url_contains('checkout-step-one')

    def click_continue_shopping(self) -> None:
        """
        Click the Continue Shopping button to return to the inventory page.

        Example:
            cart_page.click_continue_shopping()
        """
        # Navigate back to the product listing
        self.click(CONTINUE_SHOPPING_BUTTON)
        # WHY: wait for URL to confirm navigation completed before callers
        # check driver.current_url — without this the URL still shows /cart.html
        self.wait.wait_for_url_contains('/inventory.html')

    def is_on_cart_page(self) -> bool:
        """
        Check whether the browser is currently on the cart page.

        Returns:
            bool: True if the current URL contains '/cart.html'.

        Example:
            assert cart_page.is_on_cart_page()
        """
        return '/cart.html' in self.get_current_url()
