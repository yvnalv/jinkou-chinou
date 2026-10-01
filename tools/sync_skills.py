#!/usr/bin/env python3
"""Cross-platform smart synchronization tool for jinkou-chinou domain skills.

Dynamically scans domain skills and syncs them to local AI agent skill folders:
  - Gemini / Antigravity : %USERPROFILE%/.gemini/config/skills
  - Claude Code          : %USERPROFILE%/.claude/skills

Features:
  - Dynamic user profile path resolution (works for any user on any machine).
  - SHA-256 content hashing to scan first and only copy/overwrite files that changed.
  - Safe pruning of deleted files to prevent orphaned files in target directories.
  - Itemized changelog of all updated skills and modified files.

Usage:
  python tools/sync_skills.py [--dry-run] [--force] [--targets gemini,claude]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"
INSTALL_MARKER = ".installed-by-jinkou-chinou.json"

IGNORED_NAMES = {
    "__pycache__",
    ".git",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    INSTALL_MARKER,
}
IGNORED_SUFFIXES = (".pyc", ".pyo", ".tmp")


@dataclass
class SkillSource:
    name: str
    domain: str
    path: Path
    files: dict[str, str] = field(default_factory=dict)  # rel_path -> sha256


@dataclass
class TargetSyncResult:
    target_name: str
    target_path: Path
    installed_skills: list[str] = field(default_factory=list)
    updated_skills: list[str] = field(default_factory=list)
    up_to_date_skills: list[str] = field(default_factory=list)
    failed_skills: dict[str, str] = field(default_factory=dict)  # skill_name -> error_msg
    file_changes: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    skipped_reason: str | None = None


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def scan_folder(folder: Path) -> dict[str, str]:
    """Scan folder recursively and return map of rel_path -> sha256."""
    files: dict[str, str] = {}
    if not folder.is_dir():
        return files

    for root, dirs, filenames in os.walk(folder):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_NAMES]
        for filename in filenames:
            if filename in IGNORED_NAMES or filename.endswith(IGNORED_SUFFIXES):
                continue
            file_path = Path(root) / filename
            try:
                rel_path = file_path.relative_to(folder).as_posix()
                files[rel_path] = compute_sha256(file_path)
            except Exception:
                continue
    return files


def discover_domain_skills() -> list[SkillSource]:
    """Discover all domain skills containing a SKILL.md."""
    skills: list[SkillSource] = []
    if not DOMAINS_DIR.is_dir():
        return skills

    for domain_dir in sorted(DOMAINS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name in IGNORED_NAMES:
            continue
        for skill_dir in sorted(domain_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name in IGNORED_NAMES:
                continue
            if (skill_dir / "SKILL.md").is_file():
                files = scan_folder(skill_dir)
                skills.append(
                    SkillSource(
                        name=skill_dir.name,
                        domain=domain_dir.name,
                        path=skill_dir,
                        files=files,
                    )
                )
    return skills


def resolve_default_targets() -> dict[str, Path]:
    """Dynamically resolve target folders based on user's home directory."""
    home = Path.home()
    codex_home = os.environ.get("CODEX_HOME")
    legacy_codex = Path(codex_home) / "skills" if codex_home else home / ".codex" / "skills"

    targets = {
        "Gemini / Antigravity": home / ".gemini" / "config" / "skills",
        "Claude Code": home / ".claude" / "skills",
        "GitHub Copilot": home / ".copilot" / "skills",
        "OpenAI / Agent Skills (ChatGPT)": home / ".agents" / "skills",
        "OpenAI Codex": legacy_codex,
    }
    if (home / ".cline").is_dir():
        targets["Cline"] = home / ".cline" / "skills"
    if (home / ".cagent").is_dir():
        targets["CAgent"] = home / ".cagent" / "skills"

    return targets


def sync_skill_to_destination(
    skill: SkillSource,
    dest_dir: Path,
    dry_run: bool = False,
    force: bool = False,
) -> tuple[str, dict[str, list[str]]]:
    """Sync a skill to destination directory.

    Returns:
      (status, diff_dict) where status is 'installed', 'updated', or 'up-to-date'
    """
    skill_dest = dest_dir / skill.name
    diff: dict[str, list[str]] = {"added": [], "modified": [], "removed": []}

    if not skill_dest.exists():
        status = "installed"
        diff["added"] = sorted(skill.files.keys())
        if not dry_run:
            skill_dest.mkdir(parents=True, exist_ok=True)
            for rel_path in skill.files.keys():
                src_file = skill.path / rel_path
                dst_file = skill_dest / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            marker = {
                "source": str(skill.path),
                "domain": skill.domain,
                "synced_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            (skill_dest / INSTALL_MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")
        return status, diff

    # Destination exists -> scan and compare
    dest_files = scan_folder(skill_dest)

    if force:
        status = "updated"
        diff["modified"] = sorted(skill.files.keys())
        if not dry_run:
            shutil.rmtree(skill_dest)
            skill_dest.mkdir(parents=True, exist_ok=True)
            for rel_path in skill.files.keys():
                src_file = skill.path / rel_path
                dst_file = skill_dest / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            marker = {
                "source": str(skill.path),
                "domain": skill.domain,
                "synced_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            (skill_dest / INSTALL_MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")
        return status, diff

    # Diff calculation
    for rel_path, src_hash in skill.files.items():
        if rel_path not in dest_files:
            diff["added"].append(rel_path)
        elif dest_files[rel_path] != src_hash:
            diff["modified"].append(rel_path)

    for rel_path in dest_files.keys():
        if rel_path not in skill.files:
            diff["removed"].append(rel_path)

    has_changes = bool(diff["added"] or diff["modified"] or diff["removed"])

    if not has_changes:
        return "up-to-date", diff

    status = "updated"
    if not dry_run:
        # Apply additions and modifications
        for rel_path in diff["added"] + diff["modified"]:
            src_file = skill.path / rel_path
            dst_file = skill_dest / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)

        # Apply removals
        for rel_path in diff["removed"]:
            dst_file = skill_dest / rel_path
            if dst_file.is_file():
                dst_file.unlink()
            # Clean up empty parent directories
            parent = dst_file.parent
            while parent != skill_dest:
                if parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
                parent = parent.parent

        # Update marker
        marker = {
            "source": str(skill.path),
            "domain": skill.domain,
            "synced_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        (skill_dest / INSTALL_MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")

    return status, diff


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize all jinkou-chinou skills to local AI agent folders with smart change detection."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying destination files")
    parser.add_argument("--force", action="store_true", help="Force overwrite all files regardless of checksums")
    parser.add_argument("--targets", help="Comma-separated targets to sync (gemini, claude, copilot, chatgpt, codex, or custom paths)")
    parser.add_argument("--no-pause", action="store_true", help="Do not prompt to press Enter when finished")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON summary")

    args = parser.parse_args()

    default_targets = resolve_default_targets()
    active_targets: dict[str, Path] = {}

    if args.targets:
        keys = [k.strip().lower() for k in args.targets.split(",")]
        for k in keys:
            if "gemini" in k or "antigravity" in k:
                active_targets["Gemini / Antigravity"] = default_targets["Gemini / Antigravity"]
            elif "claude" in k:
                active_targets["Claude Code"] = default_targets["Claude Code"]
            elif "copilot" in k or "github" in k:
                active_targets["GitHub Copilot"] = default_targets["GitHub Copilot"]
            elif "chatgpt" in k or "agents" in k or "openai" in k:
                active_targets["OpenAI / Agent Skills (ChatGPT)"] = default_targets["OpenAI / Agent Skills (ChatGPT)"]
            elif "codex" in k:
                active_targets["OpenAI Codex"] = default_targets["OpenAI Codex"]
            else:
                p = Path(k).expanduser().resolve()
                active_targets[f"Custom ({p.name})"] = p
    else:
        active_targets = default_targets

    skills = discover_domain_skills()

    if not args.json:
        print("=" * 64)
        print("        jinkou-chinou AI Skills Smart Synchronizer")
        print("=" * 64)
        print(f"Current User Home : {Path.home()}")
        print(f"Discovered Skills : {len(skills)} domain skills")
        if args.dry_run:
            print("[DRY RUN MODE] No files will be modified on disk.")
        print("-" * 64)
        print("Sync Destinations:")
        for name, path in active_targets.items():
            print(f"  * {name:<22} -> {path}")
        print("=" * 64)
        print()

    target_results: list[TargetSyncResult] = []

    for target_name, target_path in active_targets.items():
        if not args.json:
            print(f">>> Syncing to: {target_name} ({target_path})")

        res = TargetSyncResult(target_name=target_name, target_path=target_path)

        # Ensure target folder can be created/accessed without crashing
        try:
            if not args.dry_run:
                target_path.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            res.skipped_reason = f"Could not access or create folder: {exc}"
            target_results.append(res)
            if not args.json:
                print(f"  [!] SKIPPED     : {res.skipped_reason}")
                print("                    (Continuing to remaining AI targets...)\n")
            continue

        for skill in skills:
            try:
                status, diff = sync_skill_to_destination(
                    skill, target_path, dry_run=args.dry_run, force=args.force
                )
                if status == "installed":
                    res.installed_skills.append(skill.name)
                    res.file_changes[skill.name] = diff
                    if not args.json:
                        print(f"  [+] INSTALLED   : {skill.name} ({len(diff['added'])} files)")
                elif status == "updated":
                    res.updated_skills.append(skill.name)
                    res.file_changes[skill.name] = diff
                    total_changes = len(diff["added"]) + len(diff["modified"]) + len(diff["removed"])
                    if not args.json:
                        print(f"  [~] UPDATED     : {skill.name} ({total_changes} files changed)")
                else:
                    res.up_to_date_skills.append(skill.name)
                    if not args.json:
                        print(f"  [=] UP TO DATE  : {skill.name}")
            except Exception as exc:
                res.failed_skills[skill.name] = str(exc)
                if not args.json:
                    print(f"  [!] FAILED      : {skill.name} ({exc}) - Continuing...")

        target_results.append(res)
        if not args.json:
            print()

    # Detailed Summary & Change Log
    if args.json:
        payload = {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "dry_run": args.dry_run,
            "targets": [
                {
                    "name": r.target_name,
                    "path": str(r.target_path),
                    "installed": r.installed_skills,
                    "updated": r.updated_skills,
                    "up_to_date": r.up_to_date_skills,
                    "failed": r.failed_skills,
                    "skipped_reason": r.skipped_reason,
                    "changes": r.file_changes,
                }
                for r in target_results
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print("=" * 64)
    print("                 DETAILED CHANGE LOG")
    print("=" * 64)

    any_changes = False
    for r in target_results:
        print(f"Destination: {r.target_name} [{r.target_path}]")
        if r.skipped_reason:
            print(f"  [SKIPPED] {r.skipped_reason}")
            print()
            continue

        installed_or_updated = r.installed_skills + r.updated_skills
        if not installed_or_updated and not r.failed_skills:
            print("  (No changes detected — all skills are already up to date.)")
        else:
            if installed_or_updated:
                any_changes = True
            for name in r.installed_skills:
                print(f"  * [NEW SKILL] {name}")
                for f in r.file_changes[name]["added"][:8]:
                    print(f"      + {f}")
                if len(r.file_changes[name]["added"]) > 8:
                    print(f"      + ... and {len(r.file_changes[name]['added']) - 8} more files")

            for name in r.updated_skills:
                diff = r.file_changes[name]
                print(f"  * [MODIFIED]  {name}")
                for f in diff["added"]:
                    print(f"      + added:    {f}")
                for f in diff["modified"]:
                    print(f"      ~ updated:  {f}")
                for f in diff["removed"]:
                    print(f"      - removed:  {f}")

            for name, err in r.failed_skills.items():
                print(f"  * [FAILED]    {name}: {err}")
        print()

    print("=" * 64)
    print("                    SYNC SUMMARY")
    print("=" * 64)
    for r in target_results:
        if r.skipped_reason:
            print(f"{r.target_name:<30} : SKIPPED ({r.skipped_reason})")
        else:
            fail_note = f", {len(r.failed_skills)} error(s)" if r.failed_skills else ""
            print(f"{r.target_name:<30} : {len(r.installed_skills)} installed, {len(r.updated_skills)} updated, {len(r.up_to_date_skills)} up-to-date{fail_note}")
    print("-" * 64)

    if any_changes:
        if args.dry_run:
            print("DRY RUN COMPLETE: The changes above would be applied.")
        else:
            print("SUCCESS: All skills synchronized with your local AI agents!")
    else:
        print("ALL SKILLS ARE CURRENT: No updates were needed.")

    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
