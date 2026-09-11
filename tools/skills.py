#!/usr/bin/env python3
"""Repository tooling for the jinkou-chinou skill collection.

Commands:
  list        List every skill with domain, type, and version.
  validate    Check skills against SKILL_STANDARD.md (exit code 1 on errors).
  new         Scaffold a new skill (and its domain folder if needed).
  catalog     Regenerate the skill catalog in README.md and domain READMEs.
  install     Install domain skills into ~/.claude/skills (link or copy).
  uninstall   Remove skills that this tool installed.
  package     Build dist/<name>.zip files for upload to claude.ai.

Run `python tools/skills.py <command> --help` for options.
Standard library only. The rules enforced here are defined in SKILL_STANDARD.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import stat
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"
META_DIR = ROOT / ".claude" / "skills"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
DEFAULT_TARGET = Path.home() / ".claude" / "skills"
DIST_DIR = ROOT / "dist"
INSTALL_MARKER = ".installed-by-jinkou-chinou.json"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
# A path under references/, scripts/ or assets/ that is not part of a longer path.
BUNDLED_REF_RE = re.compile(r"(?<![\w.\-/])((?:references|scripts|assets)/[\w.\-/]+)")
RESERVED_WORDS = ("claude", "anthropic")
ALLOWED_FRONTMATTER = {"name", "description", "metadata", "license", "allowed-tools", "compatibility"}
ALLOWED_TOP_LEVEL = {"SKILL.md", "README.md", "config", "references", "scripts", "assets", "evals"}
BUNDLED_DIRS = ("references", "scripts", "assets")
IGNORED_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db", "desktop.ini", INSTALL_MARKER}
IGNORED_SUFFIXES = (".pyc", ".pyo")
REQUIRED_README_SECTIONS = ("## When to use", "## Structure", "## Changelog")
MANIFEST_KEYS = ("name", "version", "description", "domain", "type")
TYPES = ("core", "specialized")
META_DOMAIN = "meta"
PLACEHOLDER = "TODO(skillsmith)"
CATALOG_MARKERS = ("<!-- catalog:start -->", "<!-- catalog:end -->")
DOMAIN_MARKERS = ("<!-- skills:start -->", "<!-- skills:end -->")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_SKILL_LINES = 500


# ---------------------------------------------------------------------------
# Minimal YAML subset (the tooling only needs top-level header keys)
# ---------------------------------------------------------------------------

def _strip_comment(value: str) -> str:
    if value.startswith("#"):
        return ""
    if value[:1] in "\"'":
        return value
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip()


def _scalar(value: str):
    value = _strip_comment(value.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [_scalar(v) for v in inner.split(",")] if inner else []
    return value


def _block_scalar(block: list[str], folded: bool) -> str:
    indent = min((len(l) - len(l.lstrip()) for l in block if l.strip()), default=0)
    body = [l[indent:] if l.strip() else "" for l in block]
    if not folded:
        return "\n".join(body)
    paragraphs, current = [], []
    for line in body:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs)


def _nested(block: list[str]):
    rows = [l for l in block if l.strip() and not l.lstrip().startswith("#")]
    if not rows:
        return ""
    indent = min(len(l) - len(l.lstrip()) for l in rows)
    top = [l.strip() for l in rows if len(l) - len(l.lstrip()) == indent]
    if all(t == "-" or t.startswith("- ") for t in top):
        return [_scalar(t[1:]) for t in top]
    if all(re.match(r"^[A-Za-z0-9_.-]+\s*:", t) for t in top):
        mapping = {}
        for t in top:
            key, _, value = t.partition(":")
            mapping[key.strip()] = _scalar(value) if value.strip() else ""
        return mapping
    return "\n".join(rows)


def parse_yaml_subset(text: str) -> dict:
    """Parse the top-level keys of a YAML document.

    Supports plain and quoted scalars, flow lists, block scalars (> and |),
    block lists of scalars, and one-level mappings of scalars. Deeper
    structures are returned as raw text or empty strings.
    """
    lines = text.lstrip("\ufeff").splitlines()
    data: dict = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#") or line[0] in " \t":
            continue
        match = re.match(r"^([A-Za-z0-9_.-]+)\s*:(?:\s+(.*))?$", line)
        if not match:
            continue
        key, rest = match.group(1), _strip_comment((match.group(2) or "").strip())
        block = []
        while i < len(lines) and (not lines[i].strip() or lines[i][0] in " \t"):
            block.append(lines[i])
            i += 1
        while block and not block[-1].strip():
            block.pop()
        if rest[:1] in (">", "|"):
            data[key] = _block_scalar(block, folded=rest.startswith(">"))
        elif rest:
            data[key] = _scalar(rest)
        else:
            data[key] = _nested(block)
    return data


def needs_quotes(value: str) -> bool:
    """True when a plain (unquoted) YAML scalar would be misparsed."""
    return (
        ": " in value
        or " #" in value
        or value.endswith(":")
        or value[:1] in "!&*?|>%@`\"'[]{},#-"
    )


def yaml_scalar(value: str) -> str:
    if not needs_quotes(value):
        return value
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def split_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]), "\n".join(lines[idx + 1:])
    return None, text


# ---------------------------------------------------------------------------
# Skill model and discovery
# ---------------------------------------------------------------------------

@dataclass
class Skill:
    path: Path
    location: str  # "domain" (domains/<domain>/<skill>) or "meta" (.claude/skills/<skill>)
    frontmatter: dict | None = None
    frontmatter_raw: str = ""
    manifest: dict = field(default_factory=dict)
    skill_text: str = ""
    load_errors: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def folder_domain(self) -> str:
        return self.path.parent.name if self.location == "domain" else META_DOMAIN

    @property
    def version(self) -> str:
        return str(self.manifest.get("version", ""))

    @property
    def type(self) -> str:
        return str(self.manifest.get("type", ""))

    @property
    def summary(self) -> str:
        return " ".join(str(self.manifest.get("description", "")).split())

    @property
    def extends(self) -> str:
        return str(self.manifest.get("extends", "") or "")

    @property
    def rel(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    @property
    def installable(self) -> bool:
        return self.location == "domain"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").lstrip("\ufeff")


def load_skill(path: Path, location: str) -> Skill:
    skill = Skill(path=path, location=location)
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        skill.load_errors.append("missing SKILL.md (every folder inside a domain must be a skill)")
    else:
        skill.skill_text = read_text(skill_md)
        fm_text, _ = split_frontmatter(skill.skill_text)
        if fm_text is not None:
            skill.frontmatter = parse_yaml_subset(fm_text)
            skill.frontmatter_raw = fm_text
    manifest = path / "config" / "skill.yaml"
    if manifest.is_file():
        skill.manifest = parse_yaml_subset(read_text(manifest))
    return skill


def domain_dirs() -> list[Path]:
    if not DOMAINS_DIR.is_dir():
        return []
    return sorted(p for p in DOMAINS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))


def discover() -> list[Skill]:
    skills = []
    for domain in domain_dirs():
        for path in sorted(p for p in domain.iterdir() if p.is_dir() and not p.name.startswith(".")):
            skills.append(load_skill(path, "domain"))
    if META_DIR.is_dir():
        for path in sorted(p for p in META_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")):
            skills.append(load_skill(path, "meta"))
    return skills


def select(skills: list[Skill], names: list[str]) -> list[Skill]:
    by_name = {s.name: s for s in skills}
    missing = [n for n in names if n not in by_name]
    if missing:
        sys.exit(f"error: unknown skill(s): {', '.join(missing)}")
    return [by_name[n] for n in names]


def bundled_files(directory: Path) -> list[Path]:
    return sorted(
        p for p in directory.rglob("*")
        if p.is_file()
        and not any(part in IGNORED_NAMES for part in p.relative_to(directory).parts)
        and not p.name.endswith(IGNORED_SUFFIXES)
    )


def major(version: str) -> int:
    return int(version.split(".")[0]) if SEMVER_RE.match(version) else 0


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def check_name(name: str, skill_type: str) -> list[str]:
    problems = []
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        problems.append(f"name '{name}' must be kebab-case (a-z, 0-9, single hyphens), max {MAX_NAME} chars")
    if any(word in name for word in RESERVED_WORDS):
        problems.append(f"name '{name}' must not contain {' or '.join(RESERVED_WORDS)}")
    if skill_type == "core" and not name.startswith("the-"):
        problems.append(f"core skill '{name}' must use the persona style 'the-<persona>'")
    if skill_type == "specialized" and name.startswith("the-"):
        problems.append(f"specialized skill '{name}' must not start with 'the-'; use a descriptive name")
    return problems


def strict_yaml_problems(fm_text: str) -> list[str]:
    """Catch frontmatter that the simple parser accepts but real YAML parsers reject."""
    problems = []
    for line in fm_text.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s+(.+)$", line)
        if match and match.group(2)[:1] not in "\"'>|" and needs_quotes(match.group(2)):
            problems.append(f"quote the value of '{match.group(1)}' (it contains YAML special characters)")
    try:
        import yaml  # optional; used only when installed
    except ImportError:
        return problems
    try:
        yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        problems.append(f"invalid YAML ({str(exc).splitlines()[0]})")
    return problems


def check_skill(skill: Skill, index: dict[str, Skill]) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []

    def err(message: str) -> None:
        issues.append(("error", message))

    def warn(message: str) -> None:
        issues.append(("warn", message))

    for message in skill.load_errors:
        err(message)
    if not skill.skill_text:
        return issues

    # SKILL.md frontmatter
    fm = skill.frontmatter
    fm_version = ""
    if fm is None:
        err("SKILL.md has no YAML frontmatter (--- name / description / metadata.version ---)")
    else:
        unknown = sorted(set(fm) - ALLOWED_FRONTMATTER)
        if unknown:
            err(f"SKILL.md frontmatter has non-portable keys: {', '.join(unknown)}")
        if fm.get("name") != skill.name:
            err(f"SKILL.md name '{fm.get('name', '')}' must equal folder name '{skill.name}'")
        description = fm.get("description")
        if not isinstance(description, str) or not description.strip():
            err("SKILL.md description is missing")
        else:
            if len(description) > MAX_DESCRIPTION:
                err(f"SKILL.md description is {len(description)} chars (max {MAX_DESCRIPTION})")
            if "<" in description or ">" in description:
                err("SKILL.md description must not contain '<' or '>'")
        metadata = fm.get("metadata")
        fm_version = str(metadata.get("version", "")) if isinstance(metadata, dict) else ""
        if not SEMVER_RE.match(fm_version):
            err("SKILL.md metadata.version must be semver (e.g. 1.0.0)")
        for problem in strict_yaml_problems(skill.frontmatter_raw):
            err(f"SKILL.md frontmatter: {problem}")

    line_count = skill.skill_text.count("\n") + 1
    if line_count > MAX_SKILL_LINES:
        warn(f"SKILL.md has {line_count} lines (keep under ~{MAX_SKILL_LINES}; move detail to references/)")

    # config/skill.yaml
    manifest_path = skill.path / "config" / "skill.yaml"
    if not manifest_path.is_file():
        err("missing config/skill.yaml")
    else:
        m = skill.manifest
        for key in MANIFEST_KEYS:
            if not str(m.get(key, "")).strip():
                err(f"config/skill.yaml is missing '{key}'")
        if m.get("name") and m.get("name") != skill.name:
            err(f"config/skill.yaml name '{m.get('name')}' must equal folder name '{skill.name}'")
        if skill.version and fm_version and skill.version != fm_version:
            err(f"version mismatch: skill.yaml {skill.version} vs SKILL.md {fm_version}")
        if m.get("domain") and m.get("domain") != skill.folder_domain:
            err(f"config/skill.yaml domain '{m.get('domain')}' must be '{skill.folder_domain}'")
        if skill.type and skill.type not in TYPES:
            err(f"config/skill.yaml type must be one of: {', '.join(TYPES)}")
        for problem in check_name(skill.name, skill.type):
            err(problem)
        if skill.extends:
            target = index.get(skill.extends)
            if skill.type != "specialized":
                err("only specialized skills may declare 'extends'")
            elif target is None:
                err(f"extends '{skill.extends}', which does not exist")
            elif target.type != "core":
                err(f"extends '{skill.extends}', which is not a core skill")
            elif target.folder_domain != skill.folder_domain:
                warn(f"extends '{skill.extends}' from another domain ({target.folder_domain})")
        requires = m.get("requires")
        if requires not in (None, "") and not (isinstance(requires, list) and all(isinstance(r, str) for r in requires)):
            err("config/skill.yaml 'requires' must be a list of strings")

    # Folder structure
    for entry in sorted(skill.path.iterdir()):
        if entry.name in IGNORED_NAMES:
            continue
        if entry.name not in ALLOWED_TOP_LEVEL:
            warn(f"unexpected top-level entry '{entry.name}' (allowed: {', '.join(sorted(ALLOWED_TOP_LEVEL))})")
    config_dir = skill.path / "config"
    if config_dir.is_dir():
        for entry in sorted(config_dir.iterdir()):
            if entry.name != "skill.yaml" and entry.name not in IGNORED_NAMES:
                warn(f"unexpected file in config/: '{entry.name}'")

    # Bundled resources: every file listed, every listed path present
    for dirname in BUNDLED_DIRS:
        directory = skill.path / dirname
        if not directory.is_dir():
            continue
        files = bundled_files(directory)
        if not files:
            warn(f"{dirname}/ is empty; add files or remove the folder")
        for path in files:
            rel = path.relative_to(skill.path).as_posix()
            if rel not in skill.skill_text:
                err(f"{rel} is not listed in SKILL.md (add it to Bundled Resources)")
    scan_text = skill.skill_text.replace("<skill-dir>/", "")
    for ref in sorted(set(BUNDLED_REF_RE.findall(scan_text))):
        ref = ref.rstrip(".,:;)")
        if not ref or ref.endswith("/") and (skill.path / ref).is_dir():
            continue
        if not (skill.path / ref).exists():
            err(f"SKILL.md mentions '{ref}', which does not exist")

    # Unfinished scaffold placeholders
    for rel in ("SKILL.md", "README.md", "config/skill.yaml", "evals/evals.json"):
        path = skill.path / rel
        if path.is_file() and PLACEHOLDER in read_text(path):
            err(f"{rel} still contains {PLACEHOLDER} placeholders")

    # README.md
    readme = skill.path / "README.md"
    if not readme.is_file():
        err("missing README.md")
    else:
        text = read_text(readme)
        for heading in REQUIRED_README_SECTIONS:
            if not re.search(rf"^{re.escape(heading)}\s*$", text, re.M | re.I):
                err(f"README.md is missing the '{heading}' section")
        changelog = re.split(r"^## Changelog\s*$", text, flags=re.M | re.I)
        if len(changelog) > 1 and skill.version and skill.version not in changelog[1]:
            warn(f"README.md Changelog has no entry for version {skill.version}")

    # evals/evals.json
    evals = skill.path / "evals" / "evals.json"
    if evals.is_file():
        try:
            cases = json.loads(read_text(evals))
        except json.JSONDecodeError as exc:
            err(f"evals/evals.json is not valid JSON: {exc}")
        else:
            if not isinstance(cases, list) or not cases:
                err("evals/evals.json must be a non-empty JSON list")
            else:
                ids = []
                for n, case in enumerate(cases, 1):
                    if not isinstance(case, dict):
                        err(f"evals case #{n} must be an object")
                        continue
                    if not isinstance(case.get("id"), str) or not isinstance(case.get("prompt"), str):
                        err(f"evals case #{n} needs string 'id' and 'prompt'")
                    if not isinstance(case.get("should_trigger"), bool):
                        err(f"evals case #{n} needs boolean 'should_trigger'")
                    ids.append(case.get("id"))
                if len(ids) != len(set(ids)):
                    err("evals/evals.json has duplicate ids")
                positives = sum(1 for c in cases if isinstance(c, dict) and c.get("should_trigger") is True)
                negatives = sum(1 for c in cases if isinstance(c, dict) and c.get("should_trigger") is False)
                if positives < 2 or negatives < 1:
                    warn("evals should have at least 2 should_trigger=true and 1 should_trigger=false cases")
    elif major(skill.version) >= 1 and (skill.path / "scripts").is_dir():
        err("skills at version >= 1.0.0 with scripts/ require evals/evals.json")
    else:
        warn("no evals/evals.json (recommended)")

    return issues


def check_repository(skills: list[Skill]) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []
    seen: dict[str, Skill] = {}
    for skill in skills:
        if skill.name in seen:
            issues.append(("error", skill.rel, f"duplicate skill name (also at {seen[skill.name].rel})"))
        seen.setdefault(skill.name, skill)

    for domain in domain_dirs():
        subject = domain.relative_to(ROOT).as_posix()
        if not NAME_RE.match(domain.name):
            issues.append(("error", subject, "domain folder name must be kebab-case"))
        if domain.name == META_DOMAIN:
            issues.append(("error", subject, "'meta' is reserved for .claude/skills/"))
        readme = domain / "README.md"
        if not readme.is_file():
            issues.append(("error", subject, "missing domain README.md"))
        else:
            text = read_text(readme)
            if not all(marker in text for marker in DOMAIN_MARKERS):
                issues.append(("error", subject, f"README.md needs {DOMAIN_MARKERS[0]} ... {DOMAIN_MARKERS[1]} markers"))
            if PLACEHOLDER in text:
                issues.append(("error", subject, f"README.md still contains {PLACEHOLDER} placeholders"))
        cores = [s.name for s in skills if s.location == "domain" and s.folder_domain == domain.name and s.type == "core"]
        if len(cores) > 1:
            issues.append(("error", subject, f"a domain has at most one core skill (found: {', '.join(cores)})"))

    stale = catalog_changes(skills)
    for path in stale:
        issues.append(("error", path.relative_to(ROOT).as_posix(), "catalog is out of date; run: python tools/skills.py catalog"))
    return issues


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _sorted_for_catalog(skills: list[Skill]) -> list[Skill]:
    return sorted(skills, key=lambda s: (s.type != "core", s.name))


def render_root_catalog(skills: list[Skill]) -> str:
    lines: list[str] = []
    by_domain: dict[str, list[Skill]] = {}
    for skill in skills:
        if skill.location == "domain":
            by_domain.setdefault(skill.folder_domain, []).append(skill)
    for domain in domain_dirs():
        by_domain.setdefault(domain.name, [])
    if not by_domain:
        lines.append("_No skills yet._")
    for domain in sorted(by_domain):
        lines += [f"### [{domain}](domains/{domain}/)", ""]
        members = _sorted_for_catalog(by_domain[domain])
        if not members:
            lines += ["_No skills yet._", ""]
            continue
        lines += ["| Skill | Type | Version | Summary |", "|---|---|---|---|"]
        for s in members:
            lines.append(f"| [`/{s.name}`]({s.rel}/) | {s.type} | {s.version} | {_cell(s.summary)} |")
        lines.append("")
    meta = [s for s in skills if s.location == "meta"]
    if meta:
        lines += ["### meta — repo-local, not installed", "", "| Skill | Version | Summary |", "|---|---|---|"]
        for s in sorted(meta, key=lambda s: s.name):
            lines.append(f"| [`/{s.name}`]({s.rel}/) | {s.version} | {_cell(s.summary)} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_domain_catalog(domain: str, skills: list[Skill]) -> str:
    members = _sorted_for_catalog([s for s in skills if s.location == "domain" and s.folder_domain == domain])
    if not members:
        return "_No skills yet._"
    lines = ["| Skill | Type | Version | Summary |", "|---|---|---|---|"]
    for s in members:
        lines.append(f"| [`/{s.name}`]({s.name}/) | {s.type} | {s.version} | {_cell(s.summary)} |")
    return "\n".join(lines)


def replace_block(text: str, markers: tuple[str, str], content: str) -> str | None:
    start, end = markers
    i, j = text.find(start), text.find(end)
    if i == -1 or j == -1 or j < i:
        return None
    return text[: i + len(start)] + "\n" + content + "\n" + text[j:]


def catalog_targets(skills: list[Skill]) -> list[tuple[Path, tuple[str, str], str]]:
    targets = [(ROOT / "README.md", CATALOG_MARKERS, render_root_catalog(skills))]
    for domain in domain_dirs():
        targets.append((domain / "README.md", DOMAIN_MARKERS, render_domain_catalog(domain.name, skills)))
    return targets


def catalog_changes(skills: list[Skill]) -> list[Path]:
    changed = []
    for path, markers, content in catalog_targets(skills):
        if not path.is_file():
            continue
        current = read_text(path)
        updated = replace_block(current, markers, content)
        if updated is not None and updated != current:
            changed.append(path)
    return changed


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    skills = discover()
    if args.json:
        rows = [
            {"name": s.name, "domain": s.folder_domain, "type": s.type, "version": s.version,
             "extends": s.extends or None, "summary": s.summary, "path": s.rel}
            for s in skills
        ]
        print(json.dumps(rows, indent=2))
        return 0
    if not skills:
        print("No skills found.")
        return 0
    widths = [max(len(x) for x in col) for col in zip(*[(s.name, s.folder_domain, s.type or "?", s.version or "?") for s in skills])]
    header = ("NAME", "DOMAIN", "TYPE", "VERSION")
    widths = [max(w, len(h)) for w, h in zip(widths, header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths)) + "  EXTENDS")
    for s in skills:
        cells = (s.name, s.folder_domain, s.type or "?", s.version or "?")
        print("  ".join(c.ljust(w) for c, w in zip(cells, widths)) + f"  {s.extends or '-'}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    skills = discover()
    index = {s.name: s for s in skills}
    targets = select(skills, args.names) if args.names else skills
    errors = warnings = 0
    for skill in targets:
        issues = check_skill(skill, index)
        e = sum(1 for level, _ in issues if level == "error")
        w = len(issues) - e
        errors, warnings = errors + e, warnings + w
        status = "FAIL" if e else ("WARN" if w else "OK")
        print(f"[{status}] {skill.rel}")
        for level, message in issues:
            print(f"    {level.upper():5} {message}")
    if not args.names:
        repo_issues = check_repository(skills)
        if repo_issues:
            print("[REPO]")
        for level, subject, message in repo_issues:
            print(f"    {level.upper():5} {subject}: {message}")
            if level == "error":
                errors += 1
            else:
                warnings += 1
    print(f"\n{len(targets)} skill(s) checked: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


def render_template(name: str, context: dict[str, str]) -> str:
    text = read_text(TEMPLATES_DIR / name)
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[a-z_]+\}\}", text)
    if leftover:
        sys.exit(f"error: template {name} has unknown placeholders: {', '.join(sorted(set(leftover)))}")
    return text


def write_new(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"  created {path.relative_to(ROOT).as_posix()}")


def cmd_new(args: argparse.Namespace) -> int:
    parts = [p for p in re.split(r"[\\/]", args.target.strip()) if p]
    if len(parts) != 2:
        sys.exit("error: target must be <domain>/<skill-name>, e.g. data-science/time-series-forecasting")
    domain, name = parts
    problems = check_name(name, args.type)
    if not NAME_RE.match(domain):
        problems.append(f"domain '{domain}' must be kebab-case")
    if domain == META_DOMAIN:
        problems.append("'meta' skills live in .claude/skills/ and are created by hand")
    skills = discover()
    index = {s.name: s for s in skills}
    if name in index:
        problems.append(f"skill '{name}' already exists at {index[name].rel}")
    if args.extends:
        if args.type != "specialized":
            problems.append("only specialized skills may use --extends")
        elif args.extends not in index or index[args.extends].type != "core":
            problems.append(f"--extends '{args.extends}' must name an existing core skill")
    if args.type == "core":
        cores = [s.name for s in skills if s.location == "domain" and s.folder_domain == domain and s.type == "core"]
        if cores:
            problems.append(f"domain '{domain}' already has a core skill: {cores[0]}")
    extra_dirs = [d.strip() for d in (args.with_dirs or "").split(",") if d.strip()]
    bad_dirs = [d for d in extra_dirs if d not in BUNDLED_DIRS]
    if bad_dirs:
        problems.append(f"--with accepts only {', '.join(BUNDLED_DIRS)} (got {', '.join(bad_dirs)})")
    for text, label in ((args.description, "--description"), (args.summary, "--summary")):
        if text and ("<" in text or ">" in text):
            problems.append(f"{label} must not contain '<' or '>'")
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    domain_dir = DOMAINS_DIR / domain
    skill_dir = domain_dir / name
    context = {
        "name": name,
        "title": name.replace("-", " ").title(),
        "domain": domain,
        "type": args.type,
        "date": dt.date.today().isoformat(),
        "summary": args.summary or f"{PLACEHOLDER}: one short sentence for the catalog.",
        "description_yaml": yaml_scalar(
            args.description or f"{PLACEHOLDER} - what this skill does and exactly when to use it."
        ),
        "extends_line": f"extends: {args.extends}\n" if args.extends else "",
        "extends_note": (
            f"\nBuilds on `{args.extends}`. Copy in any of its rules this skill depends on; it must work on its own.\n"
            if args.extends else ""
        ),
    }
    print(f"Scaffolding {skill_dir.relative_to(ROOT).as_posix()}")
    if not domain_dir.exists():
        write_new(domain_dir / "README.md", render_template("domain-README.md", context))
    write_new(skill_dir / "SKILL.md", render_template("SKILL.md", context))
    write_new(skill_dir / "README.md", render_template("README.md", context))
    write_new(skill_dir / "config" / "skill.yaml", render_template("skill.yaml", context))
    write_new(skill_dir / "evals" / "evals.json", render_template("evals.json", context))
    for dirname in extra_dirs:
        (skill_dir / dirname).mkdir(parents=True, exist_ok=True)
        print(f"  created {(skill_dir / dirname).relative_to(ROOT).as_posix()}/")
    print(
        f"\nNext: replace every {PLACEHOLDER} marker, add bundled files, then run\n"
        f"  python tools/skills.py catalog\n  python tools/skills.py validate {name}"
    )
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    skills = discover()
    problems = 0
    changed = []
    for path, markers, content in catalog_targets(skills):
        rel = path.relative_to(ROOT).as_posix()
        if not path.is_file():
            print(f"error: {rel} does not exist", file=sys.stderr)
            problems += 1
            continue
        current = read_text(path)
        updated = replace_block(current, markers, content)
        if updated is None:
            print(f"error: {rel} is missing the {markers[0]} ... {markers[1]} markers", file=sys.stderr)
            problems += 1
            continue
        if updated != current:
            changed.append(rel)
            if not args.check:
                with path.open("w", encoding="utf-8", newline="\n") as fh:
                    fh.write(updated)
    if args.check:
        for rel in changed:
            print(f"out of date: {rel}")
        if not changed and not problems:
            print("Catalog is up to date.")
        return 1 if changed or problems else 0
    for rel in changed:
        print(f"updated {rel}")
    if not changed and not problems:
        print("Catalog already up to date.")
    return 1 if problems else 0


# --- install / uninstall ---------------------------------------------------

def is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    isjunction = getattr(os.path, "isjunction", None)
    if isjunction and isjunction(path):
        return True
    if os.name == "nt" and path.exists():
        attrs = getattr(os.lstat(path), "st_file_attributes", 0)
        return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    return False


def remove_link(path: Path) -> None:
    # Remove only the link itself; never follow it into the repository.
    if os.name == "nt":
        os.rmdir(path)
    else:
        path.unlink()


def make_link(src: Path, dst: Path) -> None:
    if os.name == "nt":
        import _winapi  # CPython on Windows; junctions need no admin rights or Developer Mode

        _winapi.CreateJunction(str(src), str(dst))
    else:
        os.symlink(src, dst, target_is_directory=True)


def inside_repo(path: Path) -> bool:
    try:
        Path(os.path.realpath(path)).relative_to(Path(os.path.realpath(ROOT)))
        return True
    except ValueError:
        return False


def install_state(dst: Path) -> str:
    """Return 'absent', 'managed-link', 'managed-copy', or 'foreign'."""
    if not dst.exists() and not is_link(dst):
        return "absent"
    if is_link(dst):
        return "managed-link" if inside_repo(dst) else "foreign"
    if (dst / INSTALL_MARKER).is_file():
        return "managed-copy"
    return "foreign"


def copy_ignore(_directory: str, names: list[str]) -> set[str]:
    return {n for n in names if n in IGNORED_NAMES or n.endswith(IGNORED_SUFFIXES)}


def cmd_install(args: argparse.Namespace) -> int:
    skills = discover()
    if args.all:
        targets = [s for s in skills if s.installable]
    elif args.names:
        targets = select(skills, args.names)
    else:
        sys.exit("error: name one or more skills, or pass --all")
    index = {s.name: s for s in skills}
    target_root = Path(args.target).expanduser()
    backup_root = target_root.parent / "skills-backup"
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    failures = installed = 0
    if not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    for skill in targets:
        dst = target_root / skill.name
        if not skill.installable:
            print(f"skip   {skill.name}: meta skills are repo-local and never installed")
            continue
        errors = [m for level, m in check_skill(skill, index) if level == "error"]
        if errors and not args.no_validate:
            print(f"skip   {skill.name}: {len(errors)} validation error(s); run validate {skill.name}")
            failures += 1
            continue
        state = install_state(dst)
        if state == "managed-link" and args.mode == "link" and Path(os.path.realpath(dst)) == Path(os.path.realpath(skill.path)):
            print(f"ok     {skill.name}: already linked")
            continue
        if state == "foreign" and not args.force:
            print(f"skip   {skill.name}: {dst} exists and was not installed by this tool (use --force to back it up and replace)")
            failures += 1
            continue
        action = {"absent": "install", "managed-link": "replace", "managed-copy": "replace", "foreign": "backup+replace"}[state]
        print(f"{action:6} {skill.name} -> {dst} ({args.mode})")
        if args.dry_run:
            continue
        if state == "foreign":
            backup = backup_root / f"{skill.name}-{stamp}"
            backup_root.mkdir(parents=True, exist_ok=True)
            if is_link(dst):
                remove_link(dst)
                print(f"       removed foreign link {dst}")
            else:
                shutil.move(str(dst), str(backup))
                print(f"       backed up existing folder to {backup}")
        elif state == "managed-link":
            remove_link(dst)
        elif state == "managed-copy":
            shutil.rmtree(dst)
        if args.mode == "link":
            try:
                make_link(skill.path, dst)
            except OSError as exc:
                print(f"error  {skill.name}: could not create link ({exc}); retry with --mode copy")
                failures += 1
                continue
        else:
            shutil.copytree(skill.path, dst, ignore=copy_ignore)
            marker = {"source": str(skill.path), "version": skill.version, "installed_at": dt.datetime.now().isoformat(timespec="seconds")}
            (dst / INSTALL_MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")
        installed += 1
    if installed:
        print("\nNew skills appear in `/` autocomplete in new Claude Code sessions.")
    return 1 if failures else 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    target_root = Path(args.target).expanduser()
    failures = 0
    for name in args.names:
        dst = target_root / name
        state = install_state(dst)
        if state == "absent":
            print(f"skip   {name}: not installed")
        elif state == "foreign":
            print(f"skip   {name}: {dst} was not installed by this tool; remove it by hand if intended")
            failures += 1
        else:
            print(f"remove {name} ({state})")
            if not args.dry_run:
                remove_link(dst) if state == "managed-link" else shutil.rmtree(dst)
    return 1 if failures else 0


def cmd_package(args: argparse.Namespace) -> int:
    skills = discover()
    index = {s.name: s for s in skills}
    if args.all:
        targets = [s for s in skills if s.installable]
    elif args.names:
        targets = select(skills, args.names)
    else:
        sys.exit("error: name one or more skills, or pass --all")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for skill in targets:
        if not skill.installable:
            print(f"skip   {skill.name}: meta skills are repo-local and never packaged")
            continue
        errors = [m for level, m in check_skill(skill, index) if level == "error"]
        if errors:
            print(f"skip   {skill.name}: {len(errors)} validation error(s); run validate {skill.name}")
            failures += 1
            continue
        archive = out_dir / f"{skill.name}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in bundled_files(skill.path):
                zf.write(path, f"{skill.name}/{path.relative_to(skill.path).as_posix()}")
        print(f"built  {archive}")
    return 1 if failures else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills.py",
        description="Tooling for the jinkou-chinou skill collection (rules: SKILL_STANDARD.md).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="list every skill")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("validate", help="check skills against SKILL_STANDARD.md")
    p.add_argument("names", nargs="*", help="skills to check (default: all, plus repository checks)")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("new", help="scaffold a new skill")
    p.add_argument("target", help="<domain>/<skill-name>, e.g. data-science/time-series-forecasting")
    p.add_argument("--type", required=True, choices=TYPES)
    p.add_argument("--extends", help="core skill this specialized skill builds on")
    p.add_argument("--with", dest="with_dirs", help="comma list of optional folders: references,scripts,assets")
    p.add_argument("--summary", help="one short sentence for the catalog (skill.yaml description)")
    p.add_argument("--description", help="trigger description for SKILL.md frontmatter")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("catalog", help="regenerate the catalog in README.md files")
    p.add_argument("--check", action="store_true", help="only report whether the catalog is out of date")
    p.set_defaults(func=cmd_catalog)

    p = sub.add_parser("install", help=f"install domain skills into {DEFAULT_TARGET}")
    p.add_argument("names", nargs="*")
    p.add_argument("--all", action="store_true", help="install every domain skill")
    p.add_argument("--mode", choices=("link", "copy"), default="link",
                   help="link (default): repo edits apply immediately; copy: snapshot")
    p.add_argument("--target", default=str(DEFAULT_TARGET), help="skills directory to install into")
    p.add_argument("--force", action="store_true",
                   help="replace folders not installed by this tool (they are moved to skills-backup/ first)")
    p.add_argument("--no-validate", action="store_true", help="install even if validation fails")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("uninstall", help="remove skills installed by this tool")
    p.add_argument("names", nargs="+")
    p.add_argument("--target", default=str(DEFAULT_TARGET))
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_uninstall)

    p = sub.add_parser("package", help="build dist/<name>.zip for claude.ai upload")
    p.add_argument("names", nargs="*")
    p.add_argument("--all", action="store_true", help="package every domain skill")
    p.add_argument("--out", default=str(DIST_DIR), help="output directory")
    p.set_defaults(func=cmd_package)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
