# Codebase Audit Report

**Date:** YYYY-MM-DD
**Project:** [Project Name]

## 1. Executive Summary
Provide a 1-2 paragraph high-level overview of the codebase's current health. Highlight the most pressing concerns (e.g., "The architecture is sound, but critical security vulnerabilities exist in the authentication module").

---

## 2. Critical Blockers & Security Vulnerabilities
> [!CAUTION]
> Address these issues immediately before deploying or scaling the application.

* **[Issue Title]:** Description of the security risk or critical blocker.
  * *Location:* `path/to/file.ext:Lxx-Lyy`
  * *Impact:* Why this is dangerous (e.g., SQL Injection risk).
  * *Solution:* Actionable fix.

---

## 3. Performance Bottlenecks
> [!WARNING]
> These issues will degrade system performance at scale.

* **[Issue Title]:** Description of the performance flaw.
  * *Location:* `path/to/file.ext:Lxx-Lyy`
  * *Impact:* E.g., N+1 query slowing down the user dashboard.
  * *Solution:* Actionable fix (e.g., use `.prefetch_related()` or eager loading).

---

## 4. Code Quality & Architectural Flaws
> [!NOTE]
> Resolving these issues will improve maintainability and reduce future technical debt.

* **[Issue Title]:** Description of the structural problem.
  * *Location:* `path/to/file.ext:Lxx-Lyy`
  * *Impact:* E.g., High cyclomatic complexity makes the module hard to test.
  * *Solution:* Actionable fix (e.g., extract logic into a separate strategy class).

---

## 5. Technical Debt & Maintainability
> [!TIP]
> General hygiene improvements for long-term project health.

* **Test Coverage:** Overview of missing tests.
* **Dependencies:** List of outdated or vulnerable packages.
* **Documentation:** Missing README sections or undocumented complex functions.
* **Dead Code:** Unused files or variables that should be purged.

---

## 6. Actionable Improvement Plan
A prioritized checklist for the engineering team to resolve the findings.

### Immediate Priority (0-7 Days)
- [ ] Fix [Critical Security Issue]
- [ ] Resolve [Critical Performance Blocker]

### Short-Term Priority (1-4 Weeks)
- [ ] Refactor [Architectural Flaw]
- [ ] Add unit tests for [Core Module]

### Long-Term Technical Debt
- [ ] Upgrade framework version.
- [ ] Standardize linting/formatting across the repository.
