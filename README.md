# selenium-automation-framework

![Selenium Tests](https://github.com/bhuvesh75/selenium-automation-framework/actions/workflows/selenium-tests.yml/badge.svg)

A production-grade Selenium WebDriver test automation framework built with Python 3.11, pytest, and the Page Object Model (POM) design pattern. Targets the [Sauce Demo](https://www.saucedemo.com) web application.

---

## Overview

This framework provides a structured, maintainable, and scalable approach to UI test automation. It includes:

- **Page Object Model (POM)** architecture for clean separation between test logic and page interactions
- **Data-driven testing** with pytest parametrize
- **Rich HTML reports** via pytest-html and Allure with embedded failure screenshots
- **CI/CD integration** with GitHub Actions and headless Chrome support
- **Configurable execution** via environment variables and `.env` file support
- **Automatic screenshot capture** on test failure for quick debugging

---

## Tech Stack

| Technology          | Version  | Purpose                                    |
|---------------------|----------|--------------------------------------------|
| Python              | 3.11     | Programming language                       |
| Selenium WebDriver  | 4.21.0   | Browser automation                         |
| pytest              | 8.2.2    | Test runner, fixtures, parametrize          |
| pytest-html         | 4.1.1    | HTML test execution reports                |
| Allure pytest       | 2.13.5   | Rich test reporting with dashboards        |
| WebDriver Manager   | 4.0.1    | Automatic chromedriver/geckodriver download |
| python-dotenv       | 1.0.1    | Environment variable management            |
| Faker               | 25.2.0   | Realistic test data generation             |

---

## Architecture

```
Page Object Model (POM) Design Pattern
───────────────────────────────────────

  Test Classes          Page Objects           Utilities
  ┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
  │ test_login   │─────>│ LoginPage    │─────>│ WaitHelper      │
  │ test_invent. │─────>│ InventoryPage│─────>│ ConfigReader    │
  │ test_cart    │─────>│ CartPage     │─────>│ DriverFactory   │
  │ test_checkout│─────>│ CheckoutPage │─────>│ ScreenshotUtil  │
  └──────┬───────┘      └──────┬───────┘      └─────────────────┘
         │                     │
         v                     v
  ┌─────────────┐      ┌──────────────┐
  │  conftest   │      │  BasePage    │
  │ (fixtures)  │      │ (common ops) │
  └─────────────┘      └──────────────┘
```

**Why POM?** Each web page is represented by a Python class. Locators and interactions are encapsulated in page objects, so when the UI changes, only the affected page object needs updating — not every test that uses that page.

---

## Folder Structure

```
selenium-automation-framework/
├── .github/
│   └── workflows/
│       └── selenium-tests.yml          # GitHub Actions CI pipeline
├── src/
│   ├── config/
│   │   └── config.py                   # Central configuration loader
│   ├── pages/
│   │   ├── base_page.py                # Common page interactions
│   │   ├── login_page.py               # Login page object
│   │   ├── inventory_page.py           # Products page object
│   │   ├── cart_page.py                # Cart page object
│   │   └── checkout_page.py            # Checkout flow page object
│   └── utils/
│       ├── driver_factory.py           # WebDriver creation
│       ├── wait_helper.py              # Explicit/fluent wait utilities
│       ├── screenshot_util.py          # Screenshot capture on failure
│       └── config_reader.py            # Configuration access helpers
├── tests/
│   ├── conftest.py                     # pytest fixtures (driver, screenshots)
│   ├── smoke/
│   │   └── test_smoke.py              # Quick sanity checks
│   ├── functional/
│   │   ├── test_login.py              # Login scenarios (data-driven)
│   │   ├── test_inventory.py          # Product listing and sort tests
│   │   ├── test_cart.py               # Cart add/remove tests
│   │   └── test_checkout.py           # E2E checkout flow tests
│   └── regression/
│       └── test_regression.py         # Full user journey regression
├── reports/                            # Generated at runtime (gitignored)
│   └── screenshots/                    # Failure screenshots
├── .env.example                        # Environment variable template
├── .gitignore                          # Git exclusions
├── requirements.txt                    # Python dependencies
├── pytest.ini                          # pytest configuration
├── README.md                           # This file
└── CONTRIBUTING.md                     # Contribution guidelines
```

---

## Prerequisites

- **Python 3.11** or higher — [Download](https://www.python.org/downloads/)
- **Chrome** or **Firefox** browser installed
- **pip** — Python package manager (included with Python)
- **Git** — for cloning the repository

Verify your setup:
```bash
python --version   # Should show 3.11+
pip --version      # Should show pip for Python 3.11+
```

---

## Setup Guide

```bash
# 1. Clone the repository
git clone https://github.com/bhuvesh75/selenium-automation-framework.git
cd selenium-automation-framework

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Copy and edit the environment file
cp .env.example .env
```

---

## Run Commands

### Run all tests
```bash
pytest
```

### Run smoke tests only
```bash
pytest tests/smoke/ -v
```

### Run functional tests only
```bash
pytest tests/functional/ -v
```

### Run regression tests only
```bash
pytest tests/regression/ -v
```

### Run by marker
```bash
pytest -m smoke
pytest -m functional
pytest -m regression
```

### Run in headless mode
```bash
HEADLESS=true pytest
```

### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run with Allure report
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Run with Firefox instead of Chrome
```bash
BROWSER=firefox pytest
```

---

## Test Coverage

### Smoke Tests (3 tests)
| Test | Description |
|------|-------------|
| `test_login_page_loads` | Verifies login page renders with all form elements |
| `test_valid_login_reaches_inventory` | Verifies login with standard_user reaches inventory |
| `test_page_title` | Verifies page title is 'Swag Labs' |

### Login Tests (6 tests)
| Test | Description |
|------|-------------|
| `test_valid_login_should_succeed` | Data-driven: standard_user, performance_glitch_user |
| `test_invalid_password_should_show_error` | Wrong password shows credential mismatch error |
| `test_locked_out_user_should_show_locked_error` | Locked-out account error message |
| `test_empty_username_should_show_required_error` | Missing username validation |
| `test_empty_password_should_show_required_error` | Missing password validation |

### Inventory Tests (4 tests)
| Test | Description |
|------|-------------|
| `test_product_count_is_six` | Product count equals 6 |
| `test_sort_a_to_z_first_item` | A-Z sort: first item is Sauce Labs Backpack |
| `test_sort_z_to_a_first_item` | Z-A sort: first item is Test.allTheThings() T-Shirt (Red) |
| `test_sort_price_low_to_high_first_item` | Price asc: first item is Sauce Labs Onesie |

### Cart Tests (3 tests)
| Test | Description |
|------|-------------|
| `test_add_two_products_shows_badge_count_two` | Badge shows correct count after adding 2 items |
| `test_remove_one_product_shows_badge_count_one` | Badge decrements on remove |
| `test_continue_shopping_returns_to_inventory` | Continue Shopping navigates back |

### Checkout Tests (3 tests)
| Test | Description |
|------|-------------|
| `test_full_checkout_flow_displays_confirmation` | Complete E2E purchase flow with confirmation |
| `test_order_total_contains_dollar_sign` | Total format validation |
| `test_step_navigation_reaches_step_two` | Step navigation after filling info |

### Regression Suite (1 comprehensive test)
End-to-end journey: login, browse products, sort, add to cart, verify cart, checkout, fill shipping info, verify summary, complete order, and confirm.

---

## CI/CD

The framework includes a GitHub Actions workflow (`.github/workflows/selenium-tests.yml`) that:

1. Triggers on push or pull request to the `main` branch
2. Sets up Python 3.11
3. Installs all pip dependencies
4. Installs the latest Chrome browser
5. Runs the smoke test suite in headless mode
6. Runs the functional test suite in headless mode
7. Uploads HTML reports as artifacts (always)
8. Uploads failure screenshots as artifacts (on failure only)

---

## Interpreting Reports

### pytest-html Report
After running tests with `--html`, the HTML report is generated at the specified path:

```
reports/report.html
```

The report includes:
- **Summary** — pass/fail/skip/error counts with percentages
- **Test details** — each test with its status, duration, and log output
- **Environment** — browser, platform, and Python version info

### Allure Report
After running with `--alluredir`, serve the Allure report:

```bash
allure serve allure-results
```

The Allure report includes:
- **Dashboard** — pass/fail summary with trend graphs
- **Suites** — tests grouped by module and class
- **Behaviors** — tests grouped by feature and story
- **Timeline** — execution timeline for parallel analysis

### Failure Screenshots
Screenshots are automatically captured on test failure and saved to:

```
reports/screenshots/
```

Each screenshot is named with the test function name and a timestamp for easy identification.

---

## Configuration

All configurable values are managed via environment variables (with `.env` file support):

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com` | Target application URL |
| `BROWSER` | `chrome` | Browser: `chrome` or `firefox` |
| `HEADLESS` | `false` | Headless mode: `true` or `false` |
| `IMPLICIT_WAIT` | `10` | Implicit wait timeout in seconds |
| `EXPLICIT_WAIT` | `15` | Explicit wait timeout in seconds |
| `SCREENSHOT_DIR` | `reports/screenshots` | Screenshot save directory |
| `SELENIUM_REMOTE_URL` | (empty) | Selenium Grid URL for remote execution |

---

## Author

**Bhuvesh Yadav** — QA Lead | Lead SDET | Test Automation Architect

- GitHub: [https://github.com/bhuvesh75](https://github.com/bhuvesh75)
- Certifications: ISTQB CTAL-TA, ISTQB CTFL, Certified Scrum Master
- 8+ years of experience in Quality Assurance and Automation
