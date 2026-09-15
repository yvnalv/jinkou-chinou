#!/usr/bin/env python3
"""miner_guard.py - Quality, Compliance, Drift, and Storage Guard for Web Mining.

Standard-library-only CLI tool for /the-miner.

Commands:
  check-robots       Check robots.txt permissions, crawl-delays, and sitemaps for a URL.
  validate-records   Validate extracted JSONL records against required fields, null rates, and PII.
  diff-dom           Compare baseline and current HTML snapshots to detect structural DOM drift.
  export             Export extracted records to CSV, JSON, SQL DDL/INSERTs, or SQLite database.

Usage:
  python miner_guard.py check-robots --url https://example.com/products [--user-agent MyBot]
  python miner_guard.py validate-records --data records.jsonl [--required field1,field2] [--max-null-pct 5.0]
  python miner_guard.py diff-dom --baseline base.html --current new.html [--json]
  python miner_guard.py export --data records.jsonl --format csv --out data/output.csv
  python miner_guard.py export --data records.jsonl --format sql --dialect sqlserver --out data/dump.sql
"""

from __future__ import annotations

import argparse
import csv
import html.parser
import json
import re
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import Counter
from pathlib import Path
from typing import Any

# PII regex patterns for leak detection
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")


# ---------------------------------------------------------------------------
# 1. check-robots
# ---------------------------------------------------------------------------

def cmd_check_robots(args: argparse.Namespace) -> int:
    parsed_url = urllib.parse.urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"error: invalid target URL: '{args.url}' (must include scheme, e.g. https://)", file=sys.stderr)
        return 1

    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    target_path = parsed_url.path or "/"
    if parsed_url.query:
        target_path = f"{target_path}?{parsed_url.query}"

    ua = args.user_agent or "*"
    rfp = urllib.robotparser.RobotFileParser()
    rfp.set_url(robots_url)

    req_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        req = urllib.request.Request(robots_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            rfp.parse(content.splitlines())
            status_code = resp.status
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        if exc.code == 404:
            rfp.parse([])  # 404 means no restrictions
        else:
            rfp.parse([])
    except Exception as exc:
        print(f"warning: could not fetch robots.txt ({exc}). Assuming open access with caution.", file=sys.stderr)
        status_code = 0
        rfp.parse([])

    is_allowed = rfp.can_fetch(ua, args.url)
    crawl_delay = rfp.crawl_delay(ua)
    site_maps = rfp.site_maps()

    result = {
        "target_url": args.url,
        "robots_url": robots_url,
        "status_code": status_code,
        "user_agent": ua,
        "path": target_path,
        "is_allowed": is_allowed,
        "crawl_delay": crawl_delay,
        "sitemaps": site_maps or [],
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Target URL:    {args.url}")
        print(f"Robots URL:    {robots_url} (HTTP {status_code})")
        print(f"User-Agent:    {ua}")
        print(f"Access Status: {'ALLOWED' if is_allowed else 'DISALLOWED'}")
        if crawl_delay:
            print(f"Crawl-Delay:   {crawl_delay}s")
        if site_maps:
            print(f"Sitemaps ({len(site_maps)}):")
            for sm in site_maps[:5]:
                print(f"  - {sm}")
            if len(site_maps) > 5:
                print(f"  ... and {len(site_maps) - 5} more")

    return 0 if is_allowed else 2


# ---------------------------------------------------------------------------
# 2. validate-records
# ---------------------------------------------------------------------------

def load_records(file_path: Path) -> list[dict[str, Any]]:
    records = []
    text = file_path.read_text(encoding="utf-8", errors="replace")
    if file_path.suffix.lower() == ".jsonl":
        for i, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if isinstance(rec, dict):
                    records.append(rec)
            except json.JSONDecodeError as exc:
                print(f"warning: line {i} invalid JSON ({exc})", file=sys.stderr)
    else:
        try:
            data = json.loads(text)
            if isinstance(data, list):
                records = [r for r in data if isinstance(r, dict)]
            elif isinstance(data, dict):
                records = [data]
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON file ({exc})", file=sys.stderr)
    return records


def cmd_validate_records(args: argparse.Namespace) -> int:
    path = Path(args.data)
    if not path.is_file():
        print(f"error: data file '{args.data}' not found", file=sys.stderr)
        return 1

    records = load_records(path)
    if not records:
        print("error: no valid JSON records found in file", file=sys.stderr)
        return 1

    required_fields = [f.strip() for f in args.required.split(",") if f.strip()] if args.required else []
    max_null_pct = float(args.max_null_pct) if args.max_null_pct is not None else 5.0

    field_counts = Counter()
    field_nulls = Counter()
    pii_violations = []

    for idx, rec in enumerate(records):
        for k, v in rec.items():
            field_counts[k] += 1
            if v is None or v == "" or v == [] or v == {}:
                field_nulls[k] += 1

            # Check PII in string fields
            if args.check_pii and isinstance(v, str):
                if EMAIL_REGEX.search(v) or PHONE_REGEX.search(v):
                    pii_violations.append({
                        "record_index": idx,
                        "field": k,
                        "sample": v[:50] + "..." if len(v) > 50 else v,
                    })

    total = len(records)
    all_fields = sorted(set(list(field_counts.keys()) + required_fields))
    stats = {}
    breached_fields = []

    for f in all_fields:
        present = field_counts[f]
        null_count = field_nulls[f] + (total - present)
        null_pct = round((null_count / total) * 100, 2)
        is_required = f in required_fields
        failed_threshold = is_required and (null_pct > max_null_pct)
        if failed_threshold:
            breached_fields.append(f)

        stats[f] = {
            "present_count": present,
            "null_count": null_count,
            "null_percent": null_pct,
            "is_required": is_required,
            "passed": not failed_threshold,
        }

    verdict_pass = len(breached_fields) == 0 and (not args.check_pii or len(pii_violations) == 0)

    summary = {
        "file": str(path),
        "total_records": total,
        "max_null_threshold_pct": max_null_pct,
        "fields": stats,
        "breached_fields": breached_fields,
        "pii_violations_count": len(pii_violations),
        "pii_violations": pii_violations[:10],
        "verdict": "PASS" if verdict_pass else "FAIL",
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"=== Record Validation: {path.name} (Total: {total}) ===")
        print(f"{'Field':<25} {'Status':<10} {'Nulls':<10} {'Null %':<10} {'Threshold'}")
        print("-" * 65)
        for f in all_fields:
            st = stats[f]
            status = "REQ" if st["is_required"] else "OPT"
            flag = "FAIL" if not st["passed"] else "OK"
            print(f"{f:<25} {status:<10} {st['null_count']:<10} {st['null_percent']:<9}% [{flag}]")
        print("-" * 65)
        if pii_violations:
            print(f"WARNING: {len(pii_violations)} potential PII leak(s) detected!")
        print(f"Overall Verdict: {summary['verdict']}")

    return 0 if verdict_pass else 1


# ---------------------------------------------------------------------------
# 3. diff-dom
# ---------------------------------------------------------------------------

class DOMStructureExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = Counter()
        self.ids = set()
        self.test_ids = set()
        self.json_ld_count = 0
        self.meta_tags = set()
        self.in_json_ld = False
        self.json_ld_contents = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        self.tags[tag] += 1
        attr_dict = dict(attrs)

        if "id" in attr_dict and attr_dict["id"]:
            self.ids.add(attr_dict["id"])

        for k, v in attr_dict.items():
            if k in ("data-testid", "data-qa", "data-cy", "data-test") and v:
                self.test_ids.add(v)

        if tag == "meta" and "property" in attr_dict and attr_dict["property"]:
            self.meta_tags.add(attr_dict["property"])

        if tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_count += 1

    def handle_endtag(self, tag: str):
        if tag == "script" and self.in_json_ld:
            self.in_json_ld = False

    def handle_data(self, data: str):
        if self.in_json_ld:
            clean = data.strip()
            if clean:
                self.json_ld_contents.append(clean)


def extract_dom_features(html_path: Path) -> dict[str, Any]:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    parser = DOMStructureExtractor()
    parser.feed(text)
    return {
        "tag_counts": dict(parser.tags),
        "ids": sorted(parser.ids),
        "test_ids": sorted(parser.test_ids),
        "json_ld_count": parser.json_ld_count,
        "meta_properties": sorted(parser.meta_tags),
    }


def cmd_diff_dom(args: argparse.Namespace) -> int:
    base_path = Path(args.baseline)
    curr_path = Path(args.current)

    if not base_path.is_file():
        print(f"error: baseline HTML '{args.baseline}' not found", file=sys.stderr)
        return 1
    if not curr_path.is_file():
        print(f"error: current HTML '{args.current}' not found", file=sys.stderr)
        return 1

    base = extract_dom_features(base_path)
    curr = extract_dom_features(curr_path)

    lost_ids = sorted(set(base["ids"]) - set(curr["ids"]))
    new_ids = sorted(set(curr["ids"]) - set(base["ids"]))

    lost_test_ids = sorted(set(base["test_ids"]) - set(curr["test_ids"]))
    new_test_ids = sorted(set(curr["test_ids"]) - set(base["test_ids"]))

    json_ld_diff = curr["json_ld_count"] - base["json_ld_count"]

    all_tags = sorted(set(list(base["tag_counts"].keys()) + list(curr["tag_counts"].keys())))
    tag_changes = {}
    for t in all_tags:
        b_cnt = base["tag_counts"].get(t, 0)
        c_cnt = curr["tag_counts"].get(t, 0)
        if b_cnt != c_cnt:
            tag_changes[t] = {"baseline": b_cnt, "current": c_cnt, "delta": c_cnt - b_cnt}

    has_critical_drift = len(lost_test_ids) > 0 or (base["json_ld_count"] > 0 and curr["json_ld_count"] == 0)

    report = {
        "baseline_file": str(base_path),
        "current_file": str(curr_path),
        "lost_test_ids": lost_test_ids,
        "new_test_ids": new_test_ids,
        "lost_ids": lost_ids[:20],
        "new_ids": new_ids[:20],
        "json_ld_baseline": base["json_ld_count"],
        "json_ld_current": curr["json_ld_count"],
        "json_ld_diff": json_ld_diff,
        "tag_changes": tag_changes,
        "has_critical_drift": has_critical_drift,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"=== DOM Drift Analysis: {base_path.name} -> {curr_path.name} ===")
        print(f"JSON-LD Scripts: Baseline={base['json_ld_count']} -> Current={curr['json_ld_count']}")
        if lost_test_ids:
            print(f"CRITICAL: Lost data-test IDs ({len(lost_test_ids)}): {', '.join(lost_test_ids)}")
        if lost_ids:
            print(f"Removed Element IDs ({len(lost_ids)}): {', '.join(lost_ids[:10])}...")
        if new_test_ids:
            print(f"Newly Added data-test IDs: {', '.join(new_test_ids)}")
        if not lost_test_ids and not lost_ids and json_ld_diff == 0:
            print("No major structural identifier drift detected.")

    return 1 if has_critical_drift else 0


# ---------------------------------------------------------------------------
# 4. export
# ---------------------------------------------------------------------------

def cmd_export(args: argparse.Namespace) -> int:
    path = Path(args.data)
    if not path.is_file():
        print(f"error: data file '{args.data}' not found", file=sys.stderr)
        return 1

    records = load_records(path)
    if not records:
        print("error: no valid records to export", file=sys.stderr)
        return 1

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = args.format.lower()
    table = args.table or "mined_data"
    dialect = (args.dialect or "postgres").lower()

    keys = []
    for r in records:
        for k in r.keys():
            if k not in keys:
                keys.append(k)

    if fmt == "csv":
        with out_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=keys, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for r in records:
                row = {}
                for k in keys:
                    v = r.get(k)
                    if isinstance(v, (dict, list)):
                        row[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        row[k] = v
                writer.writerow(row)
        print(f"Exported {len(records)} record(s) to CSV: {out_path}")
        return 0

    elif fmt == "json":
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2, ensure_ascii=False)
        print(f"Exported {len(records)} record(s) to JSON array: {out_path}")
        return 0

    elif fmt == "sqlite":
        conn = sqlite3.connect(str(out_path))
        cur = conn.cursor()
        col_defs = [f'"{k}" TEXT' for k in keys]
        cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(col_defs)})')
        placeholders = ", ".join(["?"] * len(keys))
        rows = []
        for r in records:
            row = []
            for k in keys:
                v = r.get(k)
                if isinstance(v, (dict, list)):
                    row.append(json.dumps(v, ensure_ascii=False))
                elif v is None:
                    row.append(None)
                else:
                    row.append(str(v))
            rows.append(row)
        cur.executemany(f'INSERT INTO "{table}" VALUES ({placeholders})', rows)
        conn.commit()
        conn.close()
        print(f"Exported {len(records)} record(s) to SQLite database: {out_path} (table '{table}')")
        return 0

    elif fmt == "sql":
        lines = []
        lines.append(f"-- SQL Export generated by miner_guard.py (Dialect: {dialect})")
        col_defs = []
        for k in keys:
            if dialect == "postgres":
                col_defs.append(f'    "{k}" TEXT')
            elif dialect == "sqlserver":
                col_defs.append(f"    [{k}] NVARCHAR(MAX)")
            else:
                col_defs.append(f'    "{k}" TEXT')

        if dialect == "sqlserver":
            lines.append(f"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{table}')")
            lines.append(f"CREATE TABLE [{table}] (")
            lines.append(",\n".join(col_defs))
            lines.append(");")
        else:
            lines.append(f'CREATE TABLE IF NOT EXISTS "{table}" (')
            lines.append(",\n".join(col_defs))
            lines.append(");")

        for r in records:
            vals = []
            for k in keys:
                v = r.get(k)
                if v is None:
                    vals.append("NULL")
                elif isinstance(v, (int, float)) and not isinstance(v, bool):
                    vals.append(str(v))
                elif isinstance(v, bool):
                    vals.append("1" if dialect == "sqlserver" else ("TRUE" if dialect == "postgres" else "1"))
                else:
                    s = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
                    s_esc = s.replace("'", "''")
                    vals.append(f"'{s_esc}'")
            if dialect == "sqlserver":
                col_names = ", ".join(f"[{k}]" for k in keys)
                lines.append(f"INSERT INTO [{table}] ({col_names}) VALUES ({', '.join(vals)});")
            else:
                col_names = ", ".join(f'"{k}"' for k in keys)
                lines.append(f'INSERT INTO "{table}" ({col_names}) VALUES ({", ".join(vals)});')

        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Exported {len(records)} record(s) to SQL script ({dialect}): {out_path}")
        return 0

    else:
        print(f"error: unsupported format '{fmt}'. Choose from: csv, json, sql, sqlite", file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="miner_guard.py",
        description="Compliance, Quality, Drift, and Storage Guard for /the-miner (SKILL_STANDARD.md compliant).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check-robots
    p_rob = sub.add_parser("check-robots", help="check target robots.txt permissions and crawl-delays")
    p_rob.add_argument("--url", required=True, help="target URL to evaluate")
    p_rob.add_argument("--user-agent", default="*", help="User-Agent name (default: '*')")
    p_rob.add_argument("--json", action="store_true", help="output machine-readable JSON")
    p_rob.set_defaults(func=cmd_check_robots)

    # validate-records
    p_val = sub.add_parser("validate-records", help="validate extracted JSON/JSONL dataset against quality rules")
    p_val.add_argument("--data", required=True, help="path to JSON or JSONL file")
    p_val.add_argument("--required", help="comma-separated list of required fields")
    p_val.add_argument("--max-null-pct", default=5.0, type=float, help="maximum allowable null percentage (default: 5.0)")
    p_val.add_argument("--check-pii", action="store_true", help="flag potential email/phone PII leaks")
    p_val.add_argument("--json", action="store_true", help="output machine-readable JSON")
    p_val.set_defaults(func=cmd_validate_records)

    # diff-dom
    p_dom = sub.add_parser("diff-dom", help="compare two HTML snapshots to detect structural DOM drift")
    p_dom.add_argument("--baseline", required=True, help="baseline HTML snapshot path")
    p_dom.add_argument("--current", required=True, help="new/current HTML snapshot path")
    p_dom.add_argument("--json", action="store_true", help="output machine-readable JSON")
    p_dom.set_defaults(func=cmd_diff_dom)

    # export
    p_exp = sub.add_parser("export", help="export records to CSV, JSON, SQL script, or SQLite database")
    p_exp.add_argument("--data", required=True, help="input JSON or JSONL file path")
    p_exp.add_argument("--format", required=True, choices=["csv", "json", "sql", "sqlite"], help="target format")
    p_exp.add_argument("--out", required=True, help="output file path")
    p_exp.add_argument("--table", default="mined_data", help="table name for SQL/SQLite (default: 'mined_data')")
    p_exp.add_argument("--dialect", choices=["postgres", "sqlserver", "sqlite"], default="postgres", help="SQL dialect for --format sql")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
