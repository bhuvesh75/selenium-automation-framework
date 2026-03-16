"""
@file        screenshot_util.py
@description Captures browser screenshots on test failure.
@purpose     Provides automated screenshot capture so failures produce
             visual evidence that can be reviewed in CI artifacts.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import os
import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from src.config.config import SCREENSHOT_DIR


def capture_screenshot(driver: WebDriver, test_name: str) -> str:
    """
    Capture a PNG screenshot and save it to the screenshots directory.

    Args:
        driver    (WebDriver): Active WebDriver session.
        test_name (str):       Name of the failing test (used in filename).

    Returns:
        str: Absolute path to the saved screenshot file.

    Example:
        path = capture_screenshot(driver, 'test_invalid_login')
    """
    # Ensure the screenshot directory exists before saving
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # Build a unique filename using the test name and a timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # Sanitise test name — replace spaces and special chars with underscores
    safe_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in test_name)
    filename = f'{safe_name}_{timestamp}.png'
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    # Save the screenshot to disk as a PNG file
    driver.save_screenshot(filepath)
    print(f'Screenshot saved: {filepath}')

    return filepath
