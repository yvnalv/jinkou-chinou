#!/usr/bin/env python3
"""
Validate the-architect planning artifacts for required files, required
headings, and obvious secret leakage.

Usage:
    python scripts/validate_artifacts.py <project_path> [--mode new|feature|migration]

Modes (see "Operating Modes" in SKILL.md):
    new        Mode A: PRD.md, ARCHITECTURE.md, IMPLEMENTATION_PLAN.md (default)
    feature    Mode B: as "new" plus PROJECT_GUIDE.md (alias: --existing)
    migration  Mode D: PROJECT_GUIDE.md, MIGRATION_BRIEF.md, ARCHITECTURE.md,
               IMPLEMENTATION_PLAN.md with rollback sections

Mode C (small change) produces no planning files, so it needs no validation.
Optional files that are present are still checked, and every artifact plus
phases/*.md is scanned for secrets.

Test traceability: every AC-xxx in the requirements document (PRD.md, or
MIGRATION_BRIEF.md in migration mode) must appear in IMPLEMENTATION_PLAN.md
or phases/*.md, and every phase file must have its test sections.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

MODES = {
    "new": ["PRD.md", "ARCHITECTURE.md", "IMPLEMENTATION_PLAN.md"],
    "feature": ["PROJECT_GUIDE.md", "PRD.md", "ARCHITECTURE.md", "IMPLEMENTATION_PLAN.md"],
    "migration": ["PROJECT_GUIDE.md", "MIGRATION_BRIEF.md", "ARCHITECTURE.md", "IMPLEMENTATION_PLAN.md"],
}

# PRD.md may be either a full product PRD or a feature-scoped PRD
# (see "Existing Project PRD Behavior" in SKILL.md).
PRD_VARIANTS = {
    "full": [
        "Product Overview", "Problem Statement", "Goals", "Non-Goals",
        "Users and Actors", "User Journeys", "Functional Requirements",
        "Business Rules", "Acceptance Criteria", "Constraints",
        "Assumptions", "Open Questions",
    ],
    "feature": [
        "Feature Name", "Current Behavior", "Expected Behavior",
        "Functional Requirements", "Business Rules", "Edge Cases",
        "Compatibility Requirements", "Acceptance Criteria",
    ],
}

HEADINGS = {
    "PROJECT_GUIDE.md": [
        "Executive Summary", "Architecture & Layering",
        "Code Style & Existing Patterns", "Application Flow",
        "Mechanized Inventories", "Contribution Rules", "Risk Matrix",
    ],
    "MIGRATION_BRIEF.md": [
        "Current State", "Target State", "Behavior to Preserve",
        "Allowed Behavior Changes", "Compatibility Requirements",
        "Safety Net", "Migration Strategy", "Rollback Plan",
        "Acceptance Criteria",
    ],
    "ARCHITECTURE.md": [
        "Architecture Summary", "Existing Architecture",
        "Target Architecture", "Testing Strategy", "Security Considerations",
    ],
    "IMPLEMENTATION_PLAN.md": [
        "Source Hierarchy", "Acceptance Criteria Coverage", "Phase Objective",
        "Current State", "Expected State", "Reference Files", "Target Files",
        "Existing Patterns to Follow", "Requirements", "Constraints",
        "Deliverables", "Tests", "Verification",
    ],
}

PHASE_HEADINGS = ["Acceptance Criteria Covered", "Tests", "Verification", "Test Evidence"]

AC_ID = re.compile(r"\bAC-\d+\b")

# Extra headings required only in a given mode.
MODE_EXTRA_HEADINGS = {
    "migration": {"IMPLEMENTATION_PLAN.md": ["Rollback / Recovery"]},
}

ALL_ARTIFACTS = ["PROJECT_GUIDE.md", "PRD.md", "MIGRATION_BRIEF.md", "ARCHITECTURE.md", "IMPLEMENTATION_PLAN.md"]

SECRET_PATTERNS = [
    re.compile(r'(?i)\b(?:api[_-]?key|password|client[_-]?secret|access[_-]?token|refresh[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9_\-./+=]{12,}'),
    re.compile(r'(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._\-+/=]{20,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
]


HEADING_LINE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$", re.MULTILINE)


def missing_headings(text: str, headings: list[str]) -> list[str]:
    # Match against Markdown heading lines only, so a phrase in body text or a
    # checklist cannot stand in for a missing section.
    heading_text = "\n".join(HEADING_LINE.findall(text)).lower()
    return [h for h in headings if h.lower() not in heading_text]


def check_secrets(label: str, text: str, errors: list[str]) -> None:
    if any(p.search(text) for p in SECRET_PATTERNS):
        errors.append(f"{label}: possible credential/secret leakage detected")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_path", nargs="?", default=".")
    parser.add_argument("--mode", choices=sorted(MODES), default="new")
    parser.add_argument("--existing", action="store_true", help="alias for --mode feature")
    args = parser.parse_args()

    mode = "feature" if args.existing and args.mode == "new" else args.mode
    root = Path(args.project_path)
    required = MODES[mode]
    extra = MODE_EXTRA_HEADINGS.get(mode, {})
    errors: list[str] = []
    texts: dict[str, str] = {}

    for filename in ALL_ARTIFACTS:
        path = root / filename
        if not path.exists():
            if filename in required:
                errors.append(f"Missing {filename} (required in {mode} mode)")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        texts[filename] = text

        if filename == "PRD.md":
            results = {name: missing_headings(text, h) for name, h in PRD_VARIANTS.items()}
            if all(results.values()):
                closest = min(results, key=lambda k: len(results[k]))
                for heading in results[closest]:
                    errors.append(f"PRD.md ({closest} PRD): missing heading '{heading}'")
        else:
            headings = HEADINGS[filename] + extra.get(filename, [])
            for heading in missing_headings(text, headings):
                errors.append(f"{filename}: missing heading '{heading}'")

        check_secrets(filename, text, errors)

    phase_texts = []
    phases = root / "phases"
    if phases.is_dir():
        for phase in sorted(phases.glob("*.md")):
            label = f"phases/{phase.name}"
            text = phase.read_text(encoding="utf-8", errors="replace")
            phase_texts.append(text)
            for heading in missing_headings(text, PHASE_HEADINGS):
                errors.append(f"{label}: missing heading '{heading}'")
            check_secrets(label, text, errors)

    # Every acceptance criterion must be traced to a test in the plan or phases.
    requirements_doc = "MIGRATION_BRIEF.md" if mode == "migration" else "PRD.md"
    if requirements_doc in texts:
        ac_ids = set(AC_ID.findall(texts[requirements_doc]))
        if not ac_ids:
            errors.append(f"{requirements_doc}: no AC-xxx identifiers found; acceptance criteria must be identified so they can be traced to tests")
        elif "IMPLEMENTATION_PLAN.md" in texts:
            traced = set(AC_ID.findall(texts["IMPLEMENTATION_PLAN.md"] + "\n".join(phase_texts)))
            for ac in sorted(ac_ids - traced, key=lambda s: int(s.split("-")[1])):
                errors.append(f"{ac} (from {requirements_doc}) is not traced to any test in IMPLEMENTATION_PLAN.md or phases/")

    if errors:
        print(f"VALIDATION FAILED ({mode} mode)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALIDATION PASSED ({mode} mode)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
