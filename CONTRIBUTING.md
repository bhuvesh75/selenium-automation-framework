# Contributing to selenium-automation-framework

Thank you for considering contributing to this project. This document outlines the conventions and workflow for submitting changes.

---

## Branch Naming

Use descriptive branch names with the following prefixes:

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feature/` | New test, page object, or utility | `feature/add-product-detail-page` |
| `bugfix/` | Bug fix in existing code | `bugfix/cart-badge-count-race-condition` |
| `test/` | New or updated test cases | `test/add-negative-checkout-tests` |
| `docs/` | Documentation updates | `docs/update-setup-guide` |

---

## Commit Message Format

Follow the conventional commit format:

```
type(scope): Brief summary (under 72 characters)

Problem: What issue or need prompted this change
Solution: How this commit addresses it
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New functionality (test, page object, utility) |
| `fix` | Bug fix |
| `test` | Adding or updating tests |
| `refactor` | Code change that does not alter behavior |
| `docs` | Documentation changes only |
| `chore` | Build, CI, or dependency changes |

### Examples

```
feat(checkout): Add negative test for missing zip code

Problem: Checkout step one has no test for empty zip code field
Solution: Add test that leaves zip empty and asserts the error message

test(login): Add data-driven tests for additional user types

Problem: Only standard_user and locked_out_user were covered
Solution: Add performance_glitch_user to the parametrize decorator
```

---

## Pull Request Checklist

Before opening a pull request, ensure:

- [ ] All new and existing tests pass locally (`HEADLESS=true pytest`)
- [ ] New test methods have Given/When/Then docstrings
- [ ] New page object methods have complete docstrings (description, Args, Returns, Example)
- [ ] Locators use module-level tuples with descriptive comments
- [ ] No hardcoded waits (`time.sleep()`) — use `WaitHelper` methods instead
- [ ] No hardcoded URLs or credentials — use `config.py` settings
- [ ] New page objects extend `BasePage`
- [ ] New test files are in the correct directory (`smoke/`, `functional/`, `regression/`)
- [ ] Code passes PEP 8 linting without errors

---

## Python Coding Standards

### General

- **Python version:** 3.11 (compatible with 3.9+)
- **Style guide:** PEP 8
- **Indentation:** 4 spaces (no tabs)
- **Line length:** 120 characters maximum
- **Imports:** One import per line, grouped in standard library / third-party / local order
- **Docstrings:** Required on all public classes and methods (Google-style or NumPy-style)
- **Type hints:** Use type hints for function parameters and return values

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | `snake_case` | `login_page.py`, `wait_helper.py` |
| Classes | `PascalCase` | `LoginPage`, `TestCart` |
| Functions/Methods | `snake_case` | `add_product_to_cart`, `get_cart_badge_count` |
| Constants | `UPPER_SNAKE_CASE` | `LOGIN_BUTTON`, `CART_BADGE` |
| Variables | `snake_case` | `inventory_page`, `badge_count` |

### Page Objects

- Extend `BasePage`
- Declare all locators as module-level tuples at the top of the file
- Comment each locator to describe which UI element it targets
- Use `BasePage` helper methods (`click`, `type`, `get_text`) — never call raw Selenium directly
- Include an `is_on_xxx_page()` method for page verification

### Test Classes

- Use `@pytest.mark.<suite>` decorators for test categorisation
- Write Given/When/Then docstrings for every test method
- Use Arrange/Act/Assert structure with inline comments
- Use `@pytest.mark.parametrize` for parameterised tests instead of duplicating test methods

### Wait Strategy

- Never use `time.sleep()` — always use `WaitHelper` methods
- Use explicit waits via `wait.wait_for_element_visible()`, `wait_for_element_clickable()`, etc.
- Timeouts come from `config.py` settings — do not hardcode seconds

---

## Adding a New Page Object

1. Create a new file in `src/pages/` (e.g., `product_detail_page.py`)
2. Add the file header with `@file`, `@description`, `@purpose`, `@author`, `@github`
3. Define locators as module-level tuples with descriptive comments
4. Create a class extending `BasePage`
5. Implement interaction methods using `BasePage` helpers
6. Add an `is_on_xxx_page()` method for page verification
7. Add complete docstrings to the class and all public methods

## Adding a New Test Class

1. Create a new file in the appropriate test directory (`smoke/`, `functional/`, `regression/`)
2. Add the file header
3. Add `@pytest.mark.<suite>` decorator to the test class
4. Write test methods with Given/When/Then docstrings
5. Use the `driver` fixture for WebDriver access
6. Use page objects for all browser interactions

---

## Questions?

Open an issue in the repository or reach out to the maintainer.
