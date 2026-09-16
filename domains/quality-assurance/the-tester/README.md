# the-tester

A language-agnostic QA and testing persona that analyzes context to choose the right testing stack, level, and tool (unit, integration, E2E) for the given codebase, and writes reliable automated tests following industry best practices.

## When to use

* You want to add tests to an existing project but aren't sure which framework to use.
* You need to write unit tests, integration tests, or end-to-end (E2E) tests.
* You need to debug or fix flaky tests.
* You want to set up a new testing suite from scratch.

Invoke with: `/the-tester`

## Structure

```text
the-tester/
├── SKILL.md                          # Core persona instructions and workflow
├── README.md                         # This file
├── config/
│   └── skill.yaml                    # Skill manifest
├── evals/
│   └── evals.json                    # Automated tests for the skill description
└── references/
    ├── test-stack-detection.md       # Guide on mapping languages to testing frameworks
    └── test-levels.md                # Guide on Unit vs Integration vs E2E
```

## Changelog

### 0.1.0 — 2026-09-16
* Initial creation of `the-tester` skill.
* Added `test-stack-detection.md` for language and stack discovery.
* Added `test-levels.md` for selecting appropriate testing levels.
