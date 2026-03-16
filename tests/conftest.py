"""
@file        conftest.py
@description pytest fixtures for the Selenium test suite.
@purpose     Provides a session-scoped or function-scoped WebDriver fixture
             that all test files can use without managing driver lifecycle themselves.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import pytest
from src.utils.driver_factory import get_driver
from src.utils.screenshot_util import capture_screenshot


@pytest.fixture(scope='function')
def driver():
    """
    pytest fixture that creates a fresh WebDriver for each test function.

    Yields:
        WebDriver: A configured Selenium WebDriver ready for browser interaction.

    Teardown:
        Quits the driver after each test, even if the test fails.
    """
    # Create a new driver instance for this test
    web_driver = get_driver()
    # Yield driver to the test — everything after yield runs as teardown
    yield web_driver
    # Quit the driver to free browser resources after each test
    web_driver.quit()


@pytest.fixture(scope='function', autouse=True)
def screenshot_on_failure(request, driver):
    """
    Auto-use fixture that captures a screenshot whenever a test fails.

    Args:
        request: pytest request object containing test metadata.
        driver:  The WebDriver instance from the driver fixture.
    """
    # yield to the test — teardown runs after
    yield
    # Check if the test failed (rep_call is set by pytest after the call phase)
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        # Capture screenshot using the test function name
        capture_screenshot(driver, request.node.name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that stores the test outcome on the request node so fixtures
    can check whether the test passed or failed.
    """
    # Execute the test and store result
    outcome = yield
    rep = outcome.get_result()
    # Attach the result to the test item so screenshot_on_failure can read it
    setattr(item, f'rep_{rep.when}', rep)
