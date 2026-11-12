#!/usr/bin/env python3
"""EoD points summary from your own Synergy Workflow remarks (references/eod-scoring.md).

Consistency, timeliness, weekly bonus and repetition penalty are computed here. Quality (0.5-3.0)
needs judgment: Claude rates each new entry once with `rate`, and the rating is kept in the
ledger (points-ledger.json next to config.json) so old weeks are never re-rated.

Usage:
  python points.py report [--weeks N | --since YYYY-MM-DD --until YYYY-MM-DD] [--env NAME]
  python points.py rate --file RATINGS.json      RATINGS: [{"key": "...", "quality": 2.5, "note": "..."}]
  python points.py ledger                        ledger summary

`report` needs playwright and the Synergy settings (it reads history read-only). Prints JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kanban_config import ConfigError, config_dir, load_config  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SIMILAR = 0.95
WEEKLY_BONUS = 2.0
REPETITION_PENALTY = 5.0


def emit(obj: dict, code: int = 0) -> int:
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    return code


# ------------------------------------------------------------------ ledger

def ledger_path() -> Path:
    return config_dir() / "points-ledger.json"


def load_ledger() -> dict:
    p = ledger_path()
    if p.is_file():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("ratings", {})
                data.setdefault("cards", {})
                return data
        except json.JSONDecodeError:
            pass
    return {"ratings": {}, "cards": {}}


def save_ledger(data: dict) -> None:
    p = ledger_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def entry_key(request_id: str, date: str, time: str, text: str) -> str:
    return hashlib.sha1(f"{request_id}|{date}|{time}|{text.strip()}".encode("utf-8")).hexdigest()[:16]


# ------------------------------------------------------------------ scoring helpers

def parse_clock(value: str) -> dt.time | None:
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*([AaPp][Mm])?\s*", value or "")
    if not m:
        return None
    h, mi, ap = int(m.group(1)), int(m.group(2)), (m.group(3) or "").lower()
    if ap == "pm" and h < 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    return dt.time(h, mi) if h < 24 and mi < 60 else None


def timeliness(entry_time: str, start_time: str | None) -> tuple[float | None, str]:
    if not start_time:
        return None, "unverified: set work_log.start_time"
    t, s = parse_clock(entry_time), parse_clock(start_time)
    if not t or not s:
        return None, "unverified: unreadable time"
    base = dt.datetime.combine(dt.date.today(), s)
    deadline, grace = (base + dt.timedelta(hours=9)).time(), (base + dt.timedelta(hours=10)).time()
    if t <= deadline:
        return 1.0, f"on time (by {deadline.strftime('%H:%M')})"
    if t <= grace:
        return 0.5, f"grace hour (after {deadline.strftime('%H:%M')})"
    return 0.0, f"late (after {grace.strftime('%H:%M')})"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def prev_workday(d: dt.date) -> dt.date:
    d -= dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def week_start(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


# ------------------------------------------------------------------ report

def build_report(collected: dict, start_time: str | None, ledger: dict, today: dt.date) -> dict:
    # One task entry per card per day: all of that day's remarks together (quality), timed by the
    # first one (timeliness: the update was in by then).
    tasks = []
    excluded = []
    for card in collected["cards"]:
        waiting = "waiting" in (card.get("status") or "").lower()
        by_day: dict[str, list] = {}
        for e in card.get("entries", []):
            by_day.setdefault(e["date"], []).append(e)
        for day, es in by_day.items():
            es = sorted(es, key=lambda e: parse_clock(e["time"]) or dt.time(0, 0))
            text = "\n\n".join(e["text"] for e in es)
            d = dt.date.fromisoformat(day)
            base = {"date": day, "weekday": d.strftime("%a"), "time": es[0]["time"],
                    "request_id": card["request_id"], "request_number": card.get("request_number"),
                    "description": card.get("description", ""), "entries_that_day": len(es), "text": text,
                    "key": entry_key(card["request_id"], day, es[0]["time"], text)}
            if d.weekday() >= 5:
                excluded.append({**base, "reason": "weekend"})
                continue
            if waiting:
                excluded.append({**base, "reason": "card is Waiting (current status)"})
                continue
            tasks.append(base)

    unscored = []
    for t in tasks:
        tp, tnote = timeliness(t["time"], start_time)
        rating = ledger["ratings"].get(t["key"])
        q = rating["quality"] if rating else None
        t.update(consistency=1.0, timeliness=tp, timeliness_note=tnote, quality=q,
                 task_score=(min(5.0, 1.0 + tp + q) if tp is not None and q is not None else None))
        if q is None:
            unscored.append({k: t[k] for k in ("key", "date", "time", "request_number", "description", "text")})

    # repetition: 3 consecutive workdays of near-identical remarks on the same card
    penalties: dict[str, list] = {}
    by_card: dict[str, list] = {}
    for t in tasks:
        by_card.setdefault(t["request_id"], []).append(t)
    for rid, ts in by_card.items():
        ts.sort(key=lambda t: t["date"])
        streak = 1
        for prev, cur in zip(ts, ts[1:]):
            consecutive = prev_workday(dt.date.fromisoformat(cur["date"])).isoformat() == prev["date"]
            similar = difflib.SequenceMatcher(None, norm(prev["text"]), norm(cur["text"])).ratio() >= SIMILAR
            streak = streak + 1 if consecutive and similar else 1
            if streak == 3:
                wk = week_start(dt.date.fromisoformat(cur["date"])).isoformat()
                penalties.setdefault(wk, []).append({"request_number": cur["request_number"], "ending": cur["date"]})

    weeks = {}
    for t in tasks:
        wk = week_start(dt.date.fromisoformat(t["date"])).isoformat()
        weeks.setdefault(wk, []).append(t)
    out_weeks = []
    for wk in sorted(set(weeks) | set(penalties), reverse=True):
        ts = sorted(weeks.get(wk, []), key=lambda t: (t["date"], t["time"]))
        start = dt.date.fromisoformat(wk)
        weekdays = [(start + dt.timedelta(days=i)).isoformat() for i in range(5)]
        days_logged = sorted({t["date"] for t in ts})
        complete_week = today > start + dt.timedelta(days=4)
        still_open = [d for d in weekdays if d >= today.isoformat() and d not in days_logged]
        if len(days_logged) == 5:
            bonus, bonus_note = WEEKLY_BONUS, "all 5 weekdays logged"
        elif complete_week or len(days_logged) + len(still_open) < 5:
            bonus, bonus_note = 0.0, f"missed: {len(days_logged)}/5 weekdays logged"
        else:
            bonus, bonus_note = 0.0, f"pending: {len(days_logged)}/5 so far, {len(still_open)} day(s) left"
        pen = REPETITION_PENALTY * len(penalties.get(wk, []))
        scored = [t["task_score"] for t in ts if t["task_score"] is not None]
        total = round(sum(scored) + bonus - pen, 2)
        per_day = []
        for d in weekdays:
            dts = [t for t in ts if t["date"] == d]
            per_day.append({"date": d, "weekday": dt.date.fromisoformat(d).strftime("%a"), "tasks": len(dts),
                            "score": round(sum(t["task_score"] or 0 for t in dts), 2),
                            "pending_quality": sum(1 for t in dts if t["quality"] is None)})
        out_weeks.append({
            "week_of": wk, "complete": complete_week, "days": per_day,
            "task_entries": len(ts), "update_days": len(days_logged),
            "task_score_sum": round(sum(scored), 2), "bonus": bonus, "bonus_note": bonus_note,
            "penalty": -pen, "penalty_detail": penalties.get(wk, []),
            "final_score": total,
            "average_per_day": round(total / len(days_logged), 2) if days_logged else None,
            "pending_quality": sum(1 for t in ts if t["quality"] is None),
            "tasks": [{k: t[k] for k in ("date", "weekday", "time", "request_number", "description", "consistency",
                                         "timeliness", "timeliness_note", "quality", "task_score",
                                         "entries_that_day")} for t in ts],
        })
    return {"weeks": out_weeks, "unscored": unscored, "excluded": excluded}


def cmd_report(args) -> int:
    try:
        cfg = load_config(env_override=args.env)
    except ConfigError as exc:
        return emit({"status": "error", "error": str(exc)}, 1)
    today = dt.date.today()
    if args.since:
        since = dt.date.fromisoformat(args.since)
        until = dt.date.fromisoformat(args.until) if args.until else today
    else:
        since = week_start(today) - dt.timedelta(weeks=max(1, args.weeks) - 1)
        until = today
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return emit({"status": "error", "error": "playwright is not installed", "hint": "python -m pip install playwright"}, 2)
    import synergy_fill
    ledger = load_ledger()
    with sync_playwright() as p:
        collected = synergy_fill.collect_entries(p, cfg, since, until, list(ledger["cards"]))
    if collected["status"] != "ok":
        return emit(collected, 1)
    for c in collected["cards"]:  # remember cards, so cards you no longer own still count next time
        ledger["cards"][c["request_id"]] = {"request_number": c.get("request_number"), "description": c.get("description", "")}
    save_ledger(ledger)
    rep = build_report(collected, cfg["work_log"]["start_time"], ledger, today)
    return emit({"status": "ok", "environment": cfg["environment"], "me": collected["me"],
                 "period": {"since": since.isoformat(), "until": until.isoformat()},
                 "start_time": cfg["work_log"]["start_time"], "ledger": str(ledger_path()), **rep})


def cmd_rate(args) -> int:
    try:
        ratings = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return emit({"status": "error", "error": str(exc)}, 1)
    if not isinstance(ratings, list):
        return emit({"status": "error", "error": "ratings file must be a JSON list"}, 1)
    ledger = load_ledger()
    saved, rejected = 0, []
    for r in ratings:
        try:
            q = float(r["quality"])
            key = str(r["key"])
        except (KeyError, TypeError, ValueError):
            rejected.append({"item": r, "reason": "needs key and numeric quality"})
            continue
        if not 0.5 <= q <= 3.0 or not re.fullmatch(r"[0-9a-f]{16}", key):
            rejected.append({"item": r, "reason": "quality must be 0.5-3.0 and key 16 hex chars"})
            continue
        ledger["ratings"][key] = {"quality": round(q * 2) / 2, "note": str(r.get("note", ""))[:300],
                                  "rated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds")}
        saved += 1
    save_ledger(ledger)
    return emit({"status": "ok" if not rejected else "partial", "saved": saved, "rejected": rejected,
                 "ledger": str(ledger_path())}, 0 if not rejected else 1)


def cmd_ledger(_args) -> int:
    led = load_ledger()
    return emit({"status": "ok", "ledger": str(ledger_path()), "ratings": len(led["ratings"]), "cards": len(led["cards"])})


def main() -> int:
    parser = argparse.ArgumentParser(description="EoD points summary for kanban-updater.")
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("report", help="points per week from your Synergy remarks")
    r.add_argument("--weeks", type=int, default=1, help="current week plus N-1 previous weeks (default 1)")
    r.add_argument("--since")
    r.add_argument("--until")
    r.add_argument("--env")
    rt = sub.add_parser("rate", help="store quality ratings in the ledger")
    rt.add_argument("--file", required=True)
    sub.add_parser("ledger", help="ledger summary")
    args = parser.parse_args()
    return {"report": cmd_report, "rate": cmd_rate, "ledger": cmd_ledger}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
