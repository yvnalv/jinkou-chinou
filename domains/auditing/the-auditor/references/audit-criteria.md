# Codebase Audit Criteria

When conducting an audit, evaluate the codebase against the following four primary pillars. Use these criteria to identify issues and formulate actionable solutions for the `AUDIT_REPORT.md`.

## 1. Code Quality & Architecture
* **SOLID Principles:** Are the classes and functions too large? Do they have multiple reasons to change (SRP violation)? Are dependencies injected or tightly coupled?
* **DRY (Don't Repeat Yourself):** Is there excessive copy-pasting of logic? Can duplicated code be abstracted into shared utilities or base classes?
* **Naming Conventions:** Are variables, functions, and classes named descriptively? Do they follow the language's standard conventions (e.g., `camelCase` for JS, `snake_case` for Python)?
* **Modularity:** Is the codebase organized into logical domains or features, or is it a "big ball of mud" in a single directory?
* **Error Handling:** Are exceptions caught and handled properly, or are there bare `try-catch` blocks that swallow errors silently?

## 2. Performance & Scalability
* **Algorithmic Complexity:** Are there nested loops causing O(N^2) or worse performance on large datasets?
* **Database Access:** 
  * **N+1 Query Problem:** Are queries executed inside loops instead of using bulk fetches or joins?
  * **Missing Indexes:** Are frequent lookups performed on non-indexed columns?
* **Resource Leaks:** Are database connections, file handles, or network sockets properly closed after use?
* **Asset Optimization (Frontend):** Are large images, unminified scripts, or unnecessary dependencies bloating the frontend bundle?

## 3. Security
* **Secrets Management:** Are there hardcoded API keys, passwords, or tokens in the source code or committed `.env` files?
* **Injection Risks:** Is user input concatenated directly into SQL queries or executed as shell commands?
* **XSS / CSRF:** Are user inputs sanitized before being rendered in the DOM? Are forms protected by anti-CSRF tokens?
* **Dependencies:** Are there heavily outdated libraries with known CVEs?

## 4. Technical Debt & Maintainability
* **Test Coverage:** Are there unit tests or integration tests? Are the tests actually asserting behavior, or are they trivial?
* **Documentation:** Is there a `README.md` explaining how to set up the project? Are complex algorithms documented with docstrings?
* **Dead Code:** Are there unused variables, commented-out blocks of old code, or deprecated endpoints still hanging around?
* **Linting / Formatting:** Does the project use an automated formatter (like Prettier or Black) and a linter (like ESLint or Flake8)?
