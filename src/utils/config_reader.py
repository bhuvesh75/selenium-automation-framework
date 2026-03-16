"""
@file        config_reader.py
@description Utility module for reading configuration values at runtime.
@purpose     Provides helper functions to access configuration settings from
             the central config module, with validation and fallback logic.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
from src.config.config import (
    BASE_URL,
    BROWSER,
    HEADLESS,
    IMPLICIT_WAIT,
    EXPLICIT_WAIT,
    SCREENSHOT_DIR,
)


def get_base_url() -> str:
    """
    Return the base URL of the application under test.

    Returns:
        str: The configured base URL (e.g., 'https://www.saucedemo.com').

    Example:
        url = get_base_url()
    """
    return BASE_URL


def get_browser() -> str:
    """
    Return the configured browser name in lowercase.

    Returns:
        str: Browser name ('chrome' or 'firefox').

    Example:
        browser = get_browser()
    """
    return BROWSER


def is_headless() -> bool:
    """
    Return whether the browser should run in headless mode.

    Returns:
        bool: True if headless mode is enabled.

    Example:
        if is_headless():
            print('Running headless')
    """
    return HEADLESS


def get_implicit_wait() -> int:
    """
    Return the implicit wait timeout in seconds.

    Returns:
        int: Implicit wait duration.

    Example:
        timeout = get_implicit_wait()
    """
    return IMPLICIT_WAIT


def get_explicit_wait() -> int:
    """
    Return the explicit wait timeout in seconds.

    Returns:
        int: Explicit wait duration.

    Example:
        timeout = get_explicit_wait()
    """
    return EXPLICIT_WAIT


def get_screenshot_dir() -> str:
    """
    Return the directory path where failure screenshots are saved.

    Returns:
        str: Path to the screenshot directory.

    Example:
        directory = get_screenshot_dir()
    """
    return SCREENSHOT_DIR
