"""
@file        config.py
@description Central configuration loader for the Selenium test framework.
@purpose     Reads environment variables (with .env file support) and exposes
             typed settings so no test or page class ever reads env vars directly.
@author      Bhuvesh Yadav
@github      https://github.com/bhuvesh75
"""
import os
from dotenv import load_dotenv

# Load .env file from the project root — silently skipped if file not present
load_dotenv()

# ─────────────────────────────────────────────────────────────
# SECTION: Application Settings
# ─────────────────────────────────────────────────────────────

# Target application URL — all page navigations are relative to this
BASE_URL: str = os.getenv('BASE_URL', 'https://www.saucedemo.com')

# Browser selection — supports 'chrome' and 'firefox'
BROWSER: str = os.getenv('BROWSER', 'chrome').lower()

# Headless mode — set to 'true' in CI pipelines to suppress browser window
HEADLESS: bool = os.getenv('HEADLESS', 'false').lower() == 'true'

# ─────────────────────────────────────────────────────────────
# SECTION: Wait Timeouts
# ─────────────────────────────────────────────────────────────

# Implicit wait applied to every find_element call
# Reason: 10s balances page load time vs test speed for saucedemo.com
IMPLICIT_WAIT: int = int(os.getenv('IMPLICIT_WAIT', '10'))

# Explicit wait for WebDriverWait conditions
# Reason: 15s allows for AJAX-heavy interactions without masking real timeouts
EXPLICIT_WAIT: int = int(os.getenv('EXPLICIT_WAIT', '15'))

# ─────────────────────────────────────────────────────────────
# SECTION: Reporting
# ─────────────────────────────────────────────────────────────

# Directory where failure screenshots are saved
SCREENSHOT_DIR: str = os.getenv('SCREENSHOT_DIR', 'reports/screenshots')
