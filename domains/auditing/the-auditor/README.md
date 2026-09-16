# the-auditor

Codebase auditor persona. Evaluates existing code quality, performance bottlenecks, tech debt, and security vulnerabilities to generate a structured audit report.

## When to use

* You want to assess the health of a legacy codebase.
* You need a performance review of a specific module or the entire app.
* You are taking over a new project and want to know its hidden problems.
* You want to identify technical debt before a major refactor.

Invoke with: `/the-auditor`

## Structure

```text
the-auditor/
├── SKILL.md                          # Core persona instructions and workflow
├── README.md                         # This file
├── config/
│   └── skill.yaml                    # Skill manifest
├── evals/
│   └── evals.json                    # Automated tests for the skill description
└── references/
    ├── audit-criteria.md             # Checklist for code quality, performance, and security
    └── AUDIT_REPORT.template.md      # Template for the structured output report
```

## Changelog

### 0.1.0 — 2026-09-16
* Initial creation of `the-auditor` skill.
* Added `audit-criteria.md` guide for deep static and dynamic assessment.
* Added `AUDIT_REPORT.template.md` structured output template.
