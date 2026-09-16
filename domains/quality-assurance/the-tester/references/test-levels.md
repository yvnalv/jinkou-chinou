# Test Levels & Strategies

As the Tester, you must decide what *level* of testing is required based on the user's request. Avoid over-testing or under-testing.

## 1. Unit Testing
**Purpose:** Verify the smallest testable parts of an application in isolation (e.g., functions, methods, classes).
**When to use:**
* Complex algorithmic logic or calculations.
* Core business rules.
* Input validation logic.
**Rules:**
* Mock or stub external dependencies (databases, networks, file systems).
* Must be extremely fast (milliseconds).
* Focus on edge cases and failure modes, not just the happy path.

## 2. Integration Testing
**Purpose:** Verify that different modules or services work together correctly.
**When to use:**
* API endpoints and controllers.
* Database repositories and data access layers.
* Interactions with external APIs (sometimes mocked, sometimes using staging environments).
**Rules:**
* Real databases or in-memory equivalents (e.g., SQLite, Testcontainers) should be used instead of heavy mocking where possible.
* Slower than unit tests, but more confident about actual system behavior.

## 3. End-to-End (E2E) / UI Testing
**Purpose:** Verify the entire application flow from the user's perspective, running in a real environment or browser.
**When to use:**
* Critical user journeys (e.g., Login, Checkout, Registration).
* When testing cross-browser compatibility or UI responsiveness.
**Rules:**
* Use robust tools like Playwright or Selenium.
* **Avoid Flakiness:** Do not use hardcoded `sleep(5)` statements. Use proper locators and wait for elements to become visible/clickable.
* High maintenance cost; only cover the most critical paths (The Testing Pyramid).

## 4. Contract Testing
**Purpose:** Ensure two separate systems (like a frontend and backend microservice) agree on the API requests and responses.
**When to use:**
* Microservices architecture.
* When third-party API changes frequently break your app.

## Honest Testing Policy
* **Never write a tautological test** (e.g., `assert(true == true)`).
* **Fail First:** Always verify that the test fails if the underlying code is broken or not yet implemented.
* **No Swallowing Errors:** Do not catch exceptions in tests just to force them to pass. Assert that the correct exception is thrown instead.
