#!/usr/bin/env python3
"""Cross-platform smart synchronization tool for jinkou-chinou domain skills.

Dynamically scans domain skills and syncs them to local AI agent skill folders:
  - Gemini / Antigravity            : %USERPROFILE%/.gemini/config/skills
  - Claude Code                     : %USERPROFILE%/.claude/skills
  - GitHub Copilot                  : %USERPROFILE%/.copilot/skills
  - OpenAI / Agent Skills (ChatGPT) : %USERPROFILE%/.agents/skills
  - OpenAI Codex                    : %USERPROFILE%/.codex/skills

Features:
  - Dynamic user profile path resolution (works for any user on any machine).
  - SHA-256 content hashing to scan first and only copy/overwrite files that changed.
  - Safe pruning of deleted files to prevent orphaned files in target directories.
  - Per-skill version tracking (vX.Y.Z, vOld -> vNew, vX.Y.Z (modified), NEW (vX.Y.Z)).
  - Installed Skills & Version Catalog + Remote GitHub (origin/main) update check.

Usage:
  python tools/sync_skills.py [--dry-run] [--force] [--targets gemini,claude]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
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

VERSION_RE = re.compile(r"^\s*version\s*:\s*[\"']?([^\"'\s#]+)[\"']?", re.MULTILINE)


@dataclass
class SkillSource:
    name: str
    domain: str
    version: str
    path: Path
    files: dict[str, str] = field(default_factory=dict)  # rel_path -> sha256


@dataclass
class SkillSyncMeta:
    name: str
    domain: str
    status: str  # 'installed', 'updated', 'up-to-date'
    prev_version: str | None
    curr_version: str
    installed_at: str
    updated_at: str
    changed_this_run: bool = False


@dataclass
class TargetSyncResult:
    target_name: str
    target_path: Path
    installed_skills: list[str] = field(default_factory=list)
    updated_skills: list[str] = field(default_factory=list)
    up_to_date_skills: list[str] = field(default_factory=list)
    failed_skills: dict[str, str] = field(default_factory=dict)  # skill_name -> error_msg
    file_changes: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    skill_meta: dict[str, SkillSyncMeta] = field(default_factory=dict)
    skipped_reason: str | None = None


def extract_skill_version(skill_dir: Path) -> str:
    """Read skill version from config/skill.yaml or SKILL.md frontmatter."""
    yaml_path = skill_dir / "config" / "skill.yaml"
    if yaml_path.is_file():
        try:
            text = yaml_path.read_text(encoding="utf-8", errors="ignore")
            m = VERSION_RE.search(text)
            if m:
                return m.group(1).strip()
        except Exception:
            pass

    md_path = skill_dir / "SKILL.md"
    if md_path.is_file():
        try:
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            m = VERSION_RE.search(text)
            if m:
                return m.group(1).strip()
        except Exception:
            pass

    return "0.1.0"


def read_install_marker(skill_dest: Path) -> dict[str, str]:
    """Read .installed-by-jinkou-chinou.json if present."""
    marker_file = skill_dest / INSTALL_MARKER
    if marker_file.is_file():
        try:
            data = json.loads(marker_file.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items() if v is not None}
        except Exception:
            pass
    return {}


def write_install_marker(
    skill_dest: Path,
    skill: SkillSource,
    installed_at: str,
    updated_at: str,
) -> None:
    """Write BOM-free UTF-8 .installed-by-jinkou-chinou.json marker."""
    marker = {
        "skill": skill.name,
        "domain": skill.domain,
        "version": skill.version,
        "source": str(skill.path),
        "installed_at": installed_at,
        "updated_at": updated_at,
        "synced_at": updated_at,
    }
    (skill_dest / INSTALL_MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")


def parse_iso_to_local(iso_str: str | None) -> dt.datetime:
    """Parse an ISO timestamp string and convert to local timezone."""
    if iso_str:
        try:
            cleaned = iso_str.strip()
            if cleaned.endswith("Z"):
                cleaned = cleaned[:-1] + "+00:00"
            parsed = dt.datetime.fromisoformat(cleaned)
            if parsed.tzinfo is not None:
                return parsed.astimezone()
            return parsed
        except Exception:
            pass
    return dt.datetime.now().astimezone()


def format_date_short(iso_str: str | None) -> str:
    return parse_iso_to_local(iso_str).strftime("%Y-%m-%d")


def format_datetime_min(iso_str: str | None) -> str:
    return parse_iso_to_local(iso_str).strftime("%Y-%m-%d %H:%M")


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
                version = extract_skill_version(skill_dir)
                skills.append(
                    SkillSource(
                        name=skill_dir.name,
                        domain=domain_dir.name,
                        version=version,
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


def fallback_file_iso(skill_dest: Path) -> str:
    """Fallback timestamp from destination SKILL.md modification time if marker lacked timestamps."""
    target_file = skill_dest / "SKILL.md"
    if not target_file.exists():
        target_file = skill_dest
    try:
        mtime = target_file.stat().st_mtime
        return dt.datetime.fromtimestamp(mtime, tz=dt.timezone.utc).isoformat()
    except Exception:
        return dt.datetime.now(dt.timezone.utc).isoformat()


def folder_created_iso(skill_dest: Path) -> str:
    """Return folder creation timestamp in UTC ISO format."""
    try:
        ctime = skill_dest.stat().st_ctime
        return dt.datetime.fromtimestamp(ctime, tz=dt.timezone.utc).isoformat()
    except Exception:
        return fallback_file_iso(skill_dest)


def sync_skill_to_destination(
    skill: SkillSource,
    dest_dir: Path,
    dry_run: bool = False,
    force: bool = False,
) -> tuple[str, dict[str, list[str]], SkillSyncMeta]:
    """Sync a skill to destination directory.

    Returns:
      (status, diff_dict, meta) where status is 'installed', 'updated', or 'up-to-date'
    """
    skill_dest = dest_dir / skill.name
    diff: dict[str, list[str]] = {"added": [], "modified": [], "removed": []}
    now_iso = dt.datetime.now(dt.timezone.utc).isoformat()

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
            write_install_marker(skill_dest, skill, installed_at=now_iso, updated_at=now_iso)
        meta = SkillSyncMeta(
            name=skill.name,
            domain=skill.domain,
            status=status,
            prev_version=None,
            curr_version=skill.version,
            installed_at=now_iso,
            updated_at=now_iso,
            changed_this_run=True,
        )
        return status, diff, meta

    # Destination exists -> inspect existing marker & version before modifying
    old_marker = read_install_marker(skill_dest)
    prev_version = old_marker.get("version") or extract_skill_version(skill_dest)
    fallback_iso = old_marker.get("synced_at") or fallback_file_iso(skill_dest)
    created_iso = folder_created_iso(skill_dest)
    raw_installed = old_marker.get("installed_at") or created_iso
    installed_at = (
        created_iso
        if parse_iso_to_local(created_iso) < parse_iso_to_local(raw_installed)
        else raw_installed
    )
    prev_updated_at = old_marker.get("updated_at") or fallback_iso

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
            write_install_marker(skill_dest, skill, installed_at=installed_at, updated_at=now_iso)
        meta = SkillSyncMeta(
            name=skill.name,
            domain=skill.domain,
            status=status,
            prev_version=prev_version,
            curr_version=skill.version,
            installed_at=installed_at,
            updated_at=now_iso,
            changed_this_run=True,
        )
        return status, diff, meta

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
        # Backfill rich marker fields if old marker was missing version/installed_at/updated_at
        if not dry_run and (
            "version" not in old_marker
            or "installed_at" not in old_marker
            or "updated_at" not in old_marker
            or old_marker.get("installed_at") != installed_at
        ):
            write_install_marker(
                skill_dest, skill, installed_at=installed_at, updated_at=prev_updated_at
            )
        meta = SkillSyncMeta(
            name=skill.name,
            domain=skill.domain,
            status="up-to-date",
            prev_version=prev_version,
            curr_version=skill.version,
            installed_at=installed_at,
            updated_at=prev_updated_at,
            changed_this_run=False,
        )
        return "up-to-date", diff, meta

    status = "updated"
    if not dry_run:
        for rel_path in diff["added"] + diff["modified"]:
            src_file = skill.path / rel_path
            dst_file = skill_dest / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)

        for rel_path in diff["removed"]:
            dst_file = skill_dest / rel_path
            if dst_file.is_file():
                dst_file.unlink()
            parent = dst_file.parent
            while parent != skill_dest:
                if parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
                parent = parent.parent

        write_install_marker(skill_dest, skill, installed_at=installed_at, updated_at=now_iso)

    meta = SkillSyncMeta(
        name=skill.name,
        domain=skill.domain,
        status=status,
        prev_version=prev_version,
        curr_version=skill.version,
        installed_at=installed_at,
        updated_at=now_iso,
        changed_this_run=True,
    )
    return status, diff, meta


def check_remote_repo_updates() -> tuple[str, int, str]:
    """Check if origin/main on GitHub has newer commits not yet pulled locally.

    Returns:
      (state, commits_ahead, latest_subject)
      where state is 'up-to-date', 'behind', or 'skipped'
    """
    if not (ROOT / ".git").exists():
        return "skipped", 0, ""
    try:
        subprocess.run(
            ["git", "fetch", "origin", "main", "--quiet"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=4,
        )
        proc = subprocess.run(
            ["git", "log", "HEAD..origin/main", "--oneline"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=3,
        )
        if proc.returncode != 0:
            return "skipped", 0, ""
        lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        if not lines:
            return "up-to-date", 0, ""
        first_subject = lines[0].split(" ", 1)[1] if " " in lines[0] else lines[0]
        return "behind", len(lines), first_subject
    except Exception:
        return "skipped", 0, ""


def aggregate_catalog_meta(
    skills: list[SkillSource], target_results: list[TargetSyncResult]
) -> list[SkillSyncMeta]:
    """Aggregate per-skill status and version across all synced targets."""
    catalog: list[SkillSyncMeta] = []
    valid_results = [r for r in target_results if not r.skipped_reason]

    for skill in skills:
        chosen: SkillSyncMeta | None = None
        for r in valid_results:
            m = r.skill_meta.get(skill.name)
            if not m:
                continue
            if chosen is None:
                chosen = m
            elif m.status == "installed" and chosen.status != "installed":
                chosen = m
            elif m.status == "updated" and chosen.status == "up-to-date":
                chosen = m
        if chosen is None:
            now_iso = dt.datetime.now(dt.timezone.utc).isoformat()
            chosen = SkillSyncMeta(
                name=skill.name,
                domain=skill.domain,
                status="up-to-date",
                prev_version=skill.version,
                curr_version=skill.version,
                installed_at=now_iso,
                updated_at=now_iso,
                changed_this_run=False,
            )
        catalog.append(chosen)
    return catalog


def format_version_display(m: SkillSyncMeta) -> str:
    if m.status == "installed":
        return f"NEW (v{m.curr_version})"
    if m.status == "updated":
        if m.prev_version and m.prev_version != m.curr_version:
            return f"v{m.prev_version} -> v{m.curr_version}"
        return f"v{m.curr_version} (modified)"
    return f"v{m.curr_version}"


def format_status_display(m: SkillSyncMeta) -> str:
    if m.status == "installed":
        return "[+] INSTALLED"
    if m.status == "updated":
        return "[~] UPDATED"
    return "[=] CURRENT"


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
        print("=" * 76)
        print("              jinkou-chinou AI Skills Smart Synchronizer")
        print("=" * 76)
        print(f"Current User Home : {Path.home()}")
        print(f"Discovered Skills : {len(skills)} domain skills")
        if args.dry_run:
            print("[DRY RUN MODE] No files will be modified on disk.")
        print("-" * 76)
        print("Sync Destinations:")
        for name, path in active_targets.items():
            print(f"  * {name:<32} -> {path}")
        print("=" * 76)
        print()

    target_results: list[TargetSyncResult] = []

    for target_name, target_path in active_targets.items():
        if not args.json:
            print(f">>> Syncing to: {target_name} ({target_path})")

        res = TargetSyncResult(target_name=target_name, target_path=target_path)

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
                status, diff, meta = sync_skill_to_destination(
                    skill, target_path, dry_run=args.dry_run, force=args.force
                )
                res.skill_meta[skill.name] = meta
                ver_label = format_version_display(meta)
                if status == "installed":
                    res.installed_skills.append(skill.name)
                    res.file_changes[skill.name] = diff
                    if not args.json:
                        print(f"  [+] INSTALLED   : {skill.name:<26} {ver_label:<18} ({len(diff['added'])} files)")
                elif status == "updated":
                    res.updated_skills.append(skill.name)
                    res.file_changes[skill.name] = diff
                    total_changes = len(diff["added"]) + len(diff["modified"]) + len(diff["removed"])
                    if not args.json:
                        print(f"  [~] UPDATED     : {skill.name:<26} {ver_label:<18} ({total_changes} files changed)")
                else:
                    res.up_to_date_skills.append(skill.name)
                    if not args.json:
                        print(f"  [=] CURRENT     : {skill.name:<26} {ver_label}")
            except Exception as exc:
                res.failed_skills[skill.name] = str(exc)
                if not args.json:
                    print(f"  [!] FAILED      : {skill.name} ({exc}) - Continuing...")

        target_results.append(res)
        if not args.json:
            print()

    catalog_meta = aggregate_catalog_meta(skills, target_results)
    remote_state, remote_ahead, remote_subj = check_remote_repo_updates()

    if args.json:
        payload = {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "dry_run": args.dry_run,
            "remote_check": {
                "state": remote_state,
                "commits_ahead": remote_ahead,
                "latest_subject": remote_subj,
            },
            "skills": [
                {
                    "name": m.name,
                    "domain": m.domain,
                    "status": m.status,
                    "prev_version": m.prev_version,
                    "version": m.curr_version,
                    "installed_at": m.installed_at,
                    "updated_at": m.updated_at,
                }
                for m in catalog_meta
            ],
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

    any_changes = any(r.installed_skills or r.updated_skills for r in target_results)

    if any_changes:
        print("=" * 76)
        print("                         DETAILED CHANGE LOG")
        print("=" * 76)
        for r in target_results:
            if r.skipped_reason or not (r.installed_skills or r.updated_skills or r.failed_skills):
                continue
            print(f"Destination: {r.target_name} [{r.target_path}]")
            for name in r.installed_skills:
                m = r.skill_meta.get(name)
                v_str = format_version_display(m) if m else ""
                print(f"  * [NEW SKILL] {name} ({v_str})")
                for f in r.file_changes[name]["added"][:6]:
                    print(f"      + {f}")
                if len(r.file_changes[name]["added"]) > 6:
                    print(f"      + ... and {len(r.file_changes[name]['added']) - 6} more files")
            for name in r.updated_skills:
                m = r.skill_meta.get(name)
                v_str = format_version_display(m) if m else ""
                diff = r.file_changes[name]
                print(f"  * [MODIFIED]  {name} ({v_str})")
                for f in diff["added"]:
                    print(f"      + added:    {f}")
                for f in diff["modified"]:
                    print(f"      ~ updated:  {f}")
                for f in diff["removed"]:
                    print(f"      - removed:  {f}")
            for name, err in r.failed_skills.items():
                print(f"  * [FAILED]    {name}: {err}")
            print()

    # Bottom Viewport: Installed Skills & Version Catalog + Agent Sync Summary
    print("=" * 76)
    print("                     INSTALLED SKILLS & VERSION CATALOG")
    print("=" * 76)
    print(f"{'Skill Name':<28} {'Version':<20} {'Status':<15} {'Last Synced'}")
    print("-" * 76)
    for m in catalog_meta:
        ver_col = format_version_display(m)
        st_col = format_status_display(m)
        date_col = format_date_short(m.updated_at) + (" *" if m.changed_this_run else "")
        print(f"{m.name:<28} {ver_col:<20} {st_col:<15} {date_col}")
    print("-" * 76)

    if catalog_meta:
        latest_updated = max(catalog_meta, key=lambda x: parse_iso_to_local(x.updated_at))
        latest_added = max(catalog_meta, key=lambda x: parse_iso_to_local(x.installed_at))
        lu_ver = (
            f"v{latest_updated.prev_version} -> v{latest_updated.curr_version}"
            if latest_updated.status == "updated"
            and latest_updated.prev_version
            and latest_updated.prev_version != latest_updated.curr_version
            else f"v{latest_updated.curr_version}"
        )
        print(
            f"Latest Updated : {latest_updated.name} ({lu_ver}) on {format_datetime_min(latest_updated.updated_at)}"
        )
        print(
            f"Latest Added   : {latest_added.name} (v{latest_added.curr_version}) on {format_datetime_min(latest_added.installed_at)}"
        )

    print("=" * 76)
    print("                           AGENT SYNC SUMMARY")
    print("=" * 76)
    for r in target_results:
        if r.skipped_reason:
            print(f"{r.target_name:<31} : SKIPPED ({r.skipped_reason})")
        else:
            fail_note = f", {len(r.failed_skills)} error(s)" if r.failed_skills else ""
            print(
                f"{r.target_name:<31} : {len(r.installed_skills)} new, {len(r.updated_skills)} updated, {len(r.up_to_date_skills)} current{fail_note}"
            )
    print("-" * 76)

    if remote_state == "behind":
        print(
            f"Remote Check   : [!] UPDATE AVAILABLE ON GITHUB (origin/main is {remote_ahead} commit(s) ahead:"
        )
        print(f"                 \"{remote_subj[:58]}\")")
        print("                 -> Run 'git pull' then re-run sync-skills.bat to update!")
    elif remote_state == "up-to-date":
        print("Remote Check   : [OK] Up to date with GitHub (origin/main)")
    else:
        print("Remote Check   : [-] Offline / skipped (using local repository state)")

    if any_changes:
        total_new = max((len(r.installed_skills) for r in target_results), default=0)
        total_upd = max((len(r.updated_skills) for r in target_results), default=0)
        if args.dry_run:
            print(f"Overall Status : DRY RUN — {total_new} new, {total_upd} updated would be applied.")
        else:
            print(
                f"Overall Status : SUCCESS — {total_new} installed, {total_upd} updated across {len(target_results)} AI agents!"
            )
    else:
        print(f"Overall Status : ALL {len(skills)} SKILLS ARE CURRENT (No local updates needed)")

    print("=" * 76)
    return 0


if __name__ == "__main__":
    sys.exit(main())
