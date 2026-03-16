"""
@file        inventory_page.py
@description Page Object for the Sauce Demo inventory (products) page.
@purpose     Encapsulates all selectors and actions for the product listing,
             sorting, cart badge, and add-to-cart interactions so tests
             reference clean methods instead of raw Selenium calls.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.base_page import BasePage
from src.config.config import IMPLICIT_WAIT, EXPLICIT_WAIT

# ─────────────────────────────────────────────────────────────
# SECTION: Element Locators
# ─────────────────────────────────────────────────────────────

# Container that holds all inventory item cards
INVENTORY_LIST = (By.CLASS_NAME, 'inventory_list')

# Individual product item cards — each card has this class
INVENTORY_ITEMS = (By.CLASS_NAME, 'inventory_item')

# Product name links within item cards
ITEM_NAMES = (By.CLASS_NAME, 'inventory_item_name')

# Sort dropdown (select element) — controls product ordering
SORT_DROPDOWN = (By.CLASS_NAME, 'product_sort_container')

# Shopping cart badge — shows the number of items in the cart
CART_BADGE = (By.CLASS_NAME, 'shopping_cart_badge')

# Shopping cart link icon — navigates to the cart page
CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')

# Page title header — displays "Products" on the inventory page
PAGE_TITLE = (By.CLASS_NAME, 'title')


class InventoryPage(BasePage):
    """
    Page Object for https://www.saucedemo.com/inventory.html.

    Provides methods to interact with the product listing: counting items,
    sorting, adding products to the cart, and reading the cart badge.
    """

    def get_product_count(self) -> int:
        """
        Return the number of product items displayed on the page.

        Returns:
            int: Count of inventory item cards visible on the page.

        Example:
            assert inventory_page.get_product_count() == 6
        """
        # Wait for the inventory list container to be visible first
        self.wait.wait_for_element_visible(INVENTORY_LIST)
        # Find all inventory item elements and return the count
        items = self.driver.find_elements(*INVENTORY_ITEMS)
        return len(items)

    def sort_by(self, option_value: str) -> None:
        """
        Select a sort option from the product sort dropdown.

        Args:
            option_value (str): The value attribute of the sort option.
                Supported values:
                    'az'    — Name (A to Z)
                    'za'    — Name (Z to A)
                    'lohi'  — Price (low to high)
                    'hilo'  — Price (high to low)

        Example:
            inventory_page.sort_by('za')
        """
        # Locate the select element and wrap it with Selenium's Select helper
        dropdown_element = self.wait.wait_for_element_visible(SORT_DROPDOWN)
        select = Select(dropdown_element)
        # Select the option by its HTML value attribute
        select.select_by_value(option_value)

    def get_first_product_name(self) -> str:
        """
        Return the name of the first product in the current listing order.

        Returns:
            str: The text of the first product name element.

        Example:
            name = inventory_page.get_first_product_name()
            assert name == 'Sauce Labs Backpack'
        """
        # Find all product name elements on the page
        names = self.driver.find_elements(*ITEM_NAMES)
        # Return the text of the first element (index 0)
        return names[0].text.strip()

    def get_last_product_name(self) -> str:
        """
        Return the name of the last product in the current listing order.

        Returns:
            str: The text of the last product name element.

        Example:
            name = inventory_page.get_last_product_name()
        """
        # Find all product name elements and return the last one's text
        names = self.driver.find_elements(*ITEM_NAMES)
        return names[-1].text.strip()

    def add_product_to_cart(self, product_name: str) -> None:
        """
        Add a specific product to the cart by clicking its 'Add to cart' button.

        The method locates the product by its name, then finds the corresponding
        'Add to cart' button within the same inventory item container.

        Args:
            product_name (str): Exact product name as displayed on the page.

        Raises:
            ValueError: If no product with the given name is found.

        Example:
            inventory_page.add_product_to_cart('Sauce Labs Backpack')
        """
        # Find all inventory item containers
        items = self.driver.find_elements(*INVENTORY_ITEMS)

        for item in items:
            # Check if this item's name matches the requested product
            name_element = item.find_element(*ITEM_NAMES)
            if name_element.text.strip() == product_name:
                # Find the 'Add to cart' button within this specific item
                # WHY: saucedemo uses data-test="add-to-cart-*" on buttons — more stable
                # than class-based selectors which change across saucedemo versions
                add_button = item.find_element(By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]')
                # WHY: JS click bypasses React's event interception. A standard
                # .click() can be silently absorbed when React is mid-render
                # (e.g. after a previous add-to-cart update), causing the click
                # to not register and the button to never switch to "Remove".
                self.driver.execute_script("arguments[0].click();", add_button)

                # WHY: React updates the button from "Add to cart" to "Remove"
                # asynchronously after the click event. Without waiting for this
                # DOM change, the next action (reading the badge or clicking the
                # cart link) runs before React's state update completes, causing
                # race conditions like stale badge reads and failed cart navigation.
                # Temporarily disable implicit wait so the explicit WebDriverWait
                # polls cleanly without the 10-second implicit delay interfering.
                # WHY timeout=EXPLICIT_WAIT (15s) not 10s: CI runners are resource-
                # constrained and React's DOM update can take up to ~12s under load.
                # 15s matches the project-wide EXPLICIT_WAIT constant for consistency.
                self.driver.implicitly_wait(0)
                try:
                    WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                        lambda d: not item.find_elements(
                            By.CSS_SELECTOR, 'button[data-test^="add-to-cart"]'
                        )
                    )
                finally:
                    # Always restore implicit wait even if the wait times out
                    self.driver.implicitly_wait(IMPLICIT_WAIT)
                return

        # If we get here, no matching product was found
        raise ValueError(f"Product '{product_name}' not found on the inventory page.")

    def get_cart_badge_count(self) -> int:
        """
        Return the number shown on the shopping cart badge.

        Returns:
            int: The number of items in the cart, or 0 if no badge is visible.

        Example:
            count = inventory_page.get_cart_badge_count()
            assert count == 2
        """
        try:
            # The badge element only exists when the cart has items
            badge = self.driver.find_element(*CART_BADGE)
            return int(badge.text.strip())
        except Exception:
            # No badge means no items in cart — return 0
            return 0

    def is_on_inventory_page(self) -> bool:
        """
        Check whether the browser is currently on the inventory page.

        Returns:
            bool: True if the current URL contains '/inventory.html'.

        Example:
            assert inventory_page.is_on_inventory_page()
        """
        return '/inventory.html' in self.get_current_url()

    def go_to_cart(self) -> None:
        """
        Click the shopping cart icon and wait for cart page to load.

        Example:
            inventory_page.go_to_cart()
        """
        # WHY: Use JavaScript click instead of a standard WebDriver click for
        # cart navigation. Immediately after add_product_to_cart(), React may
        # still be updating the DOM (badge, button state). During this update
        # window a standard .click() can be intercepted or land on a stale
        # element reference, causing navigation to silently fail. JS click
        # dispatches directly to the element and bypasses overlay/interception.
        cart_link = self.wait.wait_for_element_visible(CART_LINK)
        self.driver.execute_script("arguments[0].click();", cart_link)
        # WHY: wait for URL to confirm navigation is complete before tests
        # interact with cart elements — avoids TimeoutException on cart_item
        self.wait.wait_for_url_contains('/cart.html')
