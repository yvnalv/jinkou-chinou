#!/usr/bin/env python3
"""Collect git evidence for a work log, grouped by day and by work item number.

Read-only: runs only `git log`, `git status` and `git diff --stat`. Never commits, stashes or resets.

Usage:
  python git_activity.py --repo PATH [--repo PATH ...] [--since YYYY-MM-DD] [--until YYYY-MM-DD]
                         [--author EMAIL_OR_NAME] [--all-authors]

Defaults: --since and --until are today (local time); --author is each repo's `git config user.email`.
Work item numbers are read from commit subjects/bodies (#7111, AB#7111) and from the ref the commit
was reached through (feature/7111-license-date). Prints one JSON object.
Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MSG_ITEM_RE = re.compile(r"(?:AB)?#(\d{3,6})\b")
REF_ITEM_RE = re.compile(r"(?:^|[/_\-])#?(\d{3,6})(?=$|[/_\-])")  # feature/7111-x, yovan/user-story/#7310
FIELD, RECORD = "\x1f", "\x1e"


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def work_items(subject: str, body: str, ref: str) -> list[str]:
    found = MSG_ITEM_RE.findall(subject + "\n" + body)
    clean_ref = re.sub(r"^refs/(heads|remotes/[^/]+)/", "", ref or "")
    found += REF_ITEM_RE.findall(clean_ref)
    seen: list[str] = []
    for f in found:
        if f not in seen:
            seen.append(f)
    return seen


def repo_activity(repo: Path, since: dt.date, until: dt.date, author: str | None, all_authors: bool) -> dict:
    root = Path(git(repo, "rev-parse", "--show-toplevel").strip())
    if not all_authors and not author:
        author = git(root, "config", "user.email").strip() or None
    args = [
        "log", "--all", "--source", "--no-merges",
        f"--since={since.isoformat()} 00:00", f"--until={until.isoformat()} 23:59:59",
        "--date=format-local:%Y-%m-%d %H:%M",
        f"--pretty=format:{RECORD}%H{FIELD}%S{FIELD}%ad{FIELD}%an{FIELD}%s{FIELD}%b{FIELD}",
        "--shortstat",
    ]
    if author and not all_authors:
        args.append(f"--author={author}")
    raw = git(root, *args)

    commits = []
    for rec in raw.split(RECORD):
        if not rec.strip():
            continue
        parts = rec.split(FIELD)
        if len(parts) < 7:
            continue
        sha, ref, when, who, subject, body, stat = parts[:7]
        day, _, clock = when.partition(" ")
        commits.append({
            "date": day, "time": clock, "sha": sha[:10], "ref": ref, "author": who,
            "subject": subject.strip(), "body": body.strip()[:600],
            "stat": " ".join(stat.split()),
            "work_items": work_items(subject, body, ref),
        })

    by_day: dict[str, dict[str, list]] = {}
    for c in sorted(commits, key=lambda c: (c["date"], c["time"])):
        keys = c["work_items"] or ["unlinked"]
        for k in keys:
            by_day.setdefault(c["date"], {}).setdefault(k, []).append(
                {k2: c[k2] for k2 in ("time", "sha", "ref", "subject", "body", "stat")})

    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    status = git(root, "status", "--short").splitlines()
    diff_stat = git(root, "diff", "--stat").strip().splitlines()[-1:] if status else []
    by_mtime: dict[str, int] = {}
    for line in status:
        rel = line[3:].split(" -> ")[-1].strip().strip('"')
        try:
            day_of = dt.date.fromtimestamp((root / rel).stat().st_mtime).isoformat()
        except OSError:
            continue  # deleted or unreadable
        if since.isoformat() <= day_of <= until.isoformat():
            by_mtime[day_of] = by_mtime.get(day_of, 0) + 1
    return {
        "repo": str(root),
        "current_branch": branch,
        "current_branch_work_items": work_items("", "", branch),
        "author_filter": None if all_authors else author,
        "commit_count": len(commits),
        "by_day": dict(sorted(by_day.items(), reverse=True)),
        "uncommitted": {"files": status[:50], "file_count": len(status), "diff_stat": diff_stat,
                        "modified_in_period_by_day": dict(sorted(by_mtime.items()))},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only git evidence for kanban-updater work logs.")
    parser.add_argument("--repo", action="append", required=True, help="repository path (repeatable)")
    parser.add_argument("--since", help="first day, YYYY-MM-DD (default today)")
    parser.add_argument("--until", help="last day, YYYY-MM-DD (default today)")
    parser.add_argument("--author", help="author filter (default: repo user.email)")
    parser.add_argument("--all-authors", action="store_true", help="do not filter by author")
    args = parser.parse_args()

    today = dt.date.today()
    try:
        since = dt.date.fromisoformat(args.since) if args.since else today
        until = dt.date.fromisoformat(args.until) if args.until else today
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": f"bad date: {exc}"}))
        return 1

    repos, errors = [], []
    for r in args.repo:
        try:
            repos.append(repo_activity(Path(r).expanduser(), since, until, args.author, args.all_authors))
        except (RuntimeError, FileNotFoundError) as exc:
            errors.append({"repo": r, "error": str(exc)})
    print(json.dumps({"status": "ok" if repos else "error", "since": since.isoformat(), "until": until.isoformat(),
                      "repos": repos, "errors": errors}, indent=2, ensure_ascii=False))
    return 0 if repos else 1


if __name__ == "__main__":
    sys.exit(main())
