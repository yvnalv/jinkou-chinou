#!/usr/bin/env python3
"""Exact Synergy automation for kanban-updater: find cards, read remark history, fill remarks.

The fill step types the work log into "Remarks: Workflow" with Synergy's own timestamp and then
hands the visible Edge window to the user. It never clicks Save, Approve, or any other button
except the field's own Timestamp button.

Usage:
  python synergy_fill.py check                         settings, browser and portal pre-flight
  python synergy_fill.py find NUMBER [NUMBER ...]      resolve work item / request numbers to cards
  python synergy_fill.py history TARGET [TARGET ...]   read Workflow remark history (GUID or number)
        [--days 30] [--today YYYY-MM-DD]
  python synergy_fill.py candidates [--date YYYY-MM-DD] [--max-history 12]
                                                       today's work items: git activity + your active cards
  python synergy_fill.py entries --since DATE --until DATE [--extra GUID ...]
                                                       your own remarks on your cards (for points.py)
  python synergy_fill.py fill --plan PLAN.json         open each card in visible Edge and type the remark

Common option: --env NAME  use another environment from config.json.

PLAN.json is a list of {"query": "#7111", "request_id": "<GUID>", "message": "<work log text>"}.
Every command prints one JSON object. Requires: playwright (python -m pip install playwright).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kanban_config import ConfigError, load_config, public_view  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

GUID_RE = re.compile(r"^\{?([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\}?$")
FORMATTED_RE = re.compile(r"^(\d{1,3})\.(\d{3})\.(\d{3})$")
TS_BUTTON = "button[onclick*=\"SysSetTimestamp('WorkflowComments')\"]"
REMARKS = "textarea#WorkflowComments"

# Pages through the board's own "next page" callback (action 5), lane by lane, for every Kanban
# request type, so results are not cut at the 5 cards per column the first board load returns.
BOARD_JS = """async ([term, person, url]) => {
  const app = window.kanbanApp;
  const types = String((app && (app.kanbanRequestType || app.selectedRequest)) || '')
    .split(',').map(s => s.trim()).filter(Boolean);
  // The board keeps this as the server-rendered string 'False'/'True'; send it back unchanged.
  const isCustomer = /^true$/i.test(String(app ? app.isCustomer : 'False')) ? 'True' : 'False';
  const items = [], seen = new Set();
  for (const type of types) {
    for (let page = 1; page <= 200; page++) {
      const fd = new FormData();
      const add = (k, v) => fd.append(k, v);
      add('action', '5'); add('searchText', term); add('sortBy', (app && app.sortBy) || 'startDate');
      add('sortDir', (app && app.sortDir) || 'asc'); add('isCustomer', isCustomer);
      add('customerId', app && app.customerId ? String(app.customerId) : ''); add('requestType', type);
      add('sourceName', 'Status'); add('selectedPage', String(page)); add('filterPerson', person);
      add('filterProject', ''); add('filterPriority', ''); add('filterStatus', '');
      add('filterCreatedDate', ''); add('filterStartDate', ''); add('filterEndDate', '');
      const r = await fetch(url, {method: 'POST', body: fd, credentials: 'include',
                                  headers: {'X-Requested-With': 'XMLHttpRequest'}});
      const text = await r.text();
      let j;
      try { j = JSON.parse(text); } catch (e) { return {error: 'non-JSON response (HTTP ' + r.status + ')'}; }
      if (j.isError) return {error: j.errorMessage || 'callback error'};
      const arr = Array.isArray(j.data) ? j.data : ((j.data || {}).boardItem || []);
      if (!arr.length) break;
      for (const i of arr) {
        if (seen.has(i.requestId)) continue;
        seen.add(i.requestId);
        items.push({id: i.id, requestId: i.requestId, description: i.description || '', status: i.status || '',
          flowStatus: i.flowStatus || '', owner: i.personName || '', ownerId: i.personId,
          assigned: i.personAssigned || '', project: i.project || '', startDate: i.startDate, endDate: i.endDate});
      }
    }
  }
  return {items};
}"""

WHOAMI_JS = """() => {
  const app = window.kanbanApp || {};
  const name = app.loginPersonName || '';
  const ids = (app.requestPerson || []).filter(p => p.name === name).map(p => String(p.id));
  return {name: name, person_ids: ids};
}"""

FINAL_STATUSES = {"realized", "rejected", "processed", "completed", "done", "closed", "cancelled", "canceled"}

STATE_JS = """() => {
  const t = document.getElementById('WorkflowComments');
  const f = document.getElementById('WorkflowCommentsFreeze');
  let row = '';
  const label = [...document.querySelectorAll('td,th,label,span,div')]
    .find(e => e.children.length === 0 && /^\\s*Remarks:\\s*Workflow\\s*$/i.test(e.textContent || ''));
  if (label && label.closest('tr')) row = label.closest('tr').innerText || '';
  const visible = t ? !!(t.offsetWidth || t.offsetHeight) : false;
  return {
    title: document.title,
    has_field: !!t,
    editable: !!t && visible && !t.readOnly && !t.disabled,
    textarea: t ? t.value : '',
    freeze: f ? (f.value || '') : '',
    row: row,
    auto_timestamp: (typeof SysGet === 'function') ? String(SysGet('AutoTimeStamp') || '') : '',
    has_timestamp_button: !!document.querySelector("button[onclick*=\\"SysSetTimestamp('WorkflowComments')\\"]"),
  };
}"""


# --------------------------------------------------------------------------- helpers

def emit(obj: dict, code: int = 0) -> int:
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    return code


def now_stamp() -> str:
    return dt.datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S %Z")


def stamp_regex(date_format: str) -> re.Pattern:
    date = r"\d{4}[-/.]\d{2}[-/.]\d{2}" if date_format.startswith("yyyy") else r"\d{2}[-/.]\d{2}[-/.]\d{4}"
    return re.compile(
        r"\[(?P<who>[^\[\]\n]+?) (?P<date>" + date + r") (?P<time>\d{1,2}:\d{2}(?:\s?[AaPp][Mm])?)"
        r"(?: (?P<tz>\(GMT ?[+-]\d{1,2}:\d{2}\)))?\]"
    )


def parse_stamp_date(value: str, date_format: str) -> str | None:
    parts = re.split(r"[-/.]", value)
    try:
        if date_format.startswith("yyyy"):
            y, m, d = parts
        elif date_format.startswith("mm"):
            m, d, y = parts
        else:
            d, m, y = parts
        return dt.date(int(y), int(m), int(d)).isoformat()
    except (ValueError, TypeError):
        return None


def parse_history(text: str, date_format: str) -> list[dict]:
    rx = stamp_regex(date_format)
    marks = list(rx.finditer(text))
    entries = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        entries.append({
            "date": parse_stamp_date(m.group("date"), date_format),
            "time": m.group("time"),
            "author": m.group("who").strip(),
            "text": body,
        })
    return entries


def parse_query(raw: str) -> dict:
    s = raw.strip()
    fm = FORMATTED_RE.match(s)
    if fm:
        return {"query": raw, "number": int("".join(fm.groups())), "kind": "request_number"}
    digits = s.lstrip("#").strip()
    if digits.isdigit() and len(str(int(digits))) >= 2:
        return {"query": raw, "number": int(digits), "kind": "any"}
    raise ValueError(f"'{raw}' is not a work item (#7111), request number (46493) or formatted number (00.046.493)")


def formatted_number(n: int) -> str:
    s = f"{n:08d}"
    return f"{s[:-6]}.{s[-6:-3]}.{s[-3:]}"


def classify(items: list[dict], q: dict) -> list[dict]:
    n = q["number"]
    token = re.compile(r"(?<![\d.])" + str(n) + r"(?!\d|\.\d)")  # not inside 17111 or v7111.2
    out = []
    for it in items:
        how = None
        if it["id"] == n:
            how = "request_number"
        elif q["kind"] == "any" and token.search(it["description"]):
            how = "work_item_in_description"
        if how:
            out.append({
                "match": how,
                "request_number": formatted_number(it["id"]),
                "request_id": it["requestId"],
                "description": it["description"],
                "status": it["status"],
                "flow_status": it["flowStatus"],
                "owner": it["owner"],
                "assigned": it["assigned"],
                "project": it["project"],
                "start_date": it["startDate"],
            })
    return out


def request_url(cfg: dict, guid: str) -> str:
    return f"{cfg['docs_url']}/WflRequest.aspx?BCAction=1&ID=%7b{guid}%7d"


def cdp_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False


def find_edge() -> str | None:
    try:
        from setup_environment import find_edge_executable
        return find_edge_executable()
    except Exception:
        return None


def friendly_launch_error(exc: Exception) -> str:
    msg = str(exc)
    if "ProcessSingleton" in msg or "already in use" in msg or "lock" in msg.lower():
        return ("The automation profile is open in another Edge window that has no automation port. "
                "Close that window (do not kill Edge processes), then run the command again.")
    if "Executable doesn't exist" in msg or "msedge" in msg and "not found" in msg:
        return "Microsoft Edge was not found. Run scripts/setup_environment.py --check."
    return msg.splitlines()[0][:300]


# --------------------------------------------------------------------------- browser sessions

def launch_visible_edge(cfg: dict) -> None:
    port = cfg["browser"]["cdp_port"]
    exe = find_edge()
    if not exe:
        raise RuntimeError("Microsoft Edge was not found. Run scripts/setup_environment.py --check.")
    Path(cfg["browser"]["profile"]).mkdir(parents=True, exist_ok=True)
    args = [
        exe,
        f"--user-data-dir={cfg['browser']['profile']}",
        f"--remote-debugging-port={port}",
        f"--auth-server-allowlist={cfg['host']}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ]
    kwargs: dict = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL, "close_fds": True}
    if sys.platform == "win32":
        detached = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        try:
            subprocess.Popen(args, creationflags=detached | 0x01000000, **kwargs)  # + CREATE_BREAKAWAY_FROM_JOB
        except OSError:
            subprocess.Popen(args, creationflags=detached, **kwargs)
    else:
        subprocess.Popen(args, start_new_session=True, **kwargs)
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        if cdp_alive(port):
            return
        time.sleep(0.25)  # polling a process start-up, not waiting on page state
    raise RuntimeError(
        f"Edge started but its automation port {port} did not open. The profile is probably already open in "
        "an Edge window without the port: close that window and run the command again."
    )


def attach_credentials(context, page, creds: dict) -> None:
    """Answer HTTP auth challenges on a CDP-attached page (visible mode) with the configured credentials."""
    cdp = context.new_cdp_session(page)
    tries = {"n": 0}

    def on_paused(event):
        try:
            cdp.send("Fetch.continueRequest", {"requestId": event["requestId"]})
        except Exception:
            pass

    def on_auth(event):
        tries["n"] += 1
        response = (
            {"response": "ProvideCredentials", "username": creds["username"], "password": creds["password"]}
            if tries["n"] <= 3 else {"response": "CancelAuth"}
        )
        try:
            cdp.send("Fetch.continueWithAuth", {"requestId": event["requestId"], "authChallengeResponse": response})
        except Exception:
            pass

    cdp.on("Fetch.requestPaused", on_paused)
    cdp.on("Fetch.authRequired", on_auth)
    cdp.send("Fetch.enable", {"handleAuthRequests": True, "patterns": [{"urlPattern": "*"}]})


@contextmanager
def session(p, cfg: dict, visible: bool):
    """Yield (context, mode, opened_pages). Reuses an open automation window when one exists."""
    port = cfg["browser"]["cdp_port"]
    opened: list = []
    if visible or cdp_alive(port):
        launched = False
        if not cdp_alive(port):
            launch_visible_edge(cfg)
            launched = True
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}", slow_mo=cfg["browser"]["slow_mo"] if visible else 0)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        mode = "visible-new-window" if launched else "visible-existing-window"
        try:
            yield context, mode, opened
        finally:
            if not visible:  # read-only commands tidy up their own tabs; fill leaves them for the user
                for pg in opened:
                    try:
                        pg.close()
                    except Exception:
                        pass
            if launched:
                for pg in list(context.pages):
                    try:
                        if pg.url == "about:blank" and len(context.pages) > 1:
                            pg.close()
                    except Exception:
                        pass
        return
    context = p.chromium.launch_persistent_context(
        cfg["browser"]["profile"],
        channel="msedge",
        headless=True,
        args=[f"--auth-server-allowlist={cfg['host']}"],
        http_credentials=cfg["credentials"],
    )
    try:
        yield context, "headless", opened
    finally:
        context.close()


def new_page(context, cfg: dict, mode: str, opened: list):
    page = context.new_page()
    page.set_default_timeout(cfg["browser"]["timeout_ms"])
    opened.append(page)
    if mode.startswith("visible") and cfg["credentials"]:
        attach_credentials(context, page, cfg["credentials"])
    return page


def goto_checked(page, url: str, cfg: dict) -> dict | None:
    """Navigate; return an error dict for auth walls or HTTP failures, else None."""
    resp = page.goto(url, wait_until="load", timeout=cfg["browser"]["timeout_ms"])
    status = resp.status if resp else None
    if status == 401:
        return {"error": "auth_required", "http_status": 401,
                "hint": "Synergy asked for a login. Fill username/password for this environment in the settings "
                        "file, or sign in once in the automation profile (see references/configuration.md)."}
    if status and status >= 400:
        return {"error": "http_error", "http_status": status, "url": url}
    if re.search(r"/(login|signin|logon)", page.url, re.I):
        return {"error": "auth_required", "url": page.url, "hint": "Redirected to a login page."}
    return None


def open_board(page, cfg: dict) -> dict | None:
    err = goto_checked(page, f"{cfg['docs_url']}/GLMSysKanbanBoard.aspx", cfg)
    if err:
        return err
    page.wait_for_function("() => typeof window.kanbanApp !== 'undefined'", timeout=cfg["browser"]["timeout_ms"])
    return None


def board_query(page, cfg: dict, term: str = "", person: str = "") -> dict:
    """All board cards matching `term` (request number or description) and owner `person` (comma ids)."""
    return page.evaluate(BOARD_JS, [term, person, f"{cfg['docs_url']}/GLMSysKanbanBoardCallback.aspx"])


def whoami(page, cfg: dict) -> dict:
    """Login name from the board, and the PersonID from config or from the board's person list."""
    if not cfg.get("person_id"):
        try:  # the person list arrives with the board's first callback, after the page load
            page.wait_for_function("() => window.kanbanApp && (kanbanApp.requestPerson || []).length > 0", timeout=15000)
        except Exception:
            pass
    info = page.evaluate(WHOAMI_JS)
    pid = cfg.get("person_id") or (info["person_ids"][0] if len(info["person_ids"]) == 1 else None)
    return {"name": info["name"], "person_id": pid,
            "person_id_source": "config" if cfg.get("person_id") else ("board" if pid else "unknown")}


def card_summary(it: dict) -> dict:
    return {"request_number": formatted_number(it["id"]), "request_id": it["requestId"],
            "description": it["description"], "status": it["status"], "flow_status": it["flowStatus"],
            "owner": it["owner"], "assigned": it["assigned"], "project": it["project"], "start_date": it["startDate"]}


def is_active(it: dict) -> bool:
    return (it.get("status") or "").lower() not in FINAL_STATUSES and (it.get("flow_status") or it.get("flowStatus") or "").lower() not in FINAL_STATUSES


def read_card_history(page, cfg: dict, request_id: str) -> dict:
    """Open one request page and return its state plus parsed Workflow remark entries."""
    err = goto_checked(page, request_url(cfg, request_id), cfg)
    if err:
        return {"status": "error", **err}
    state = read_state(page)
    return {"status": "ok", "state": state, "entries": parse_history(history_text(state), cfg["date_format"])}


def search_cards(page, cfg: dict, queries: list[dict]) -> list[dict]:
    results = []
    for q in queries:
        raw = board_query(page, cfg, str(q["number"]))
        if "error" in raw:
            results.append({**q, "decision": "error", "error": raw["error"], "matches": []})
            continue
        matches = classify(raw["items"], q)
        decision = "unique" if len(matches) == 1 else "ambiguous" if matches else "not_found"
        results.append({"query": q["query"], "number": q["number"], "kind": q["kind"],
                        "decision": decision, "matches": matches})
    return results


def read_state(page) -> dict:
    return page.evaluate(STATE_JS)


def history_text(state: dict) -> str:
    candidates = [state.get("textarea") or "", state.get("freeze") or "", state.get("row") or ""]
    return max(candidates, key=len)


# --------------------------------------------------------------------------- commands

def cmd_check(p, cfg: dict) -> int:
    report = {"status": "ok", "checked_at": now_stamp(), "settings": public_view(cfg),
              "automation_window_open": cdp_alive(cfg["browser"]["cdp_port"])}
    with session(p, cfg, visible=False) as (context, mode, opened):
        page = new_page(context, cfg, mode, opened)
        err = open_board(page, cfg)
        report["browser_mode"] = mode
        if err:
            report.update({"status": "error", **err})
            return emit(report, 1)
        report["portal_title"] = page.title()
        report["kanban_board"] = "reachable"
        report["me"] = whoami(page, cfg)
        if not cfg.get("person_id"):
            report["hint"] = (f"Set person_id {report['me']['person_id']} for '{cfg['environment']}' in config.json."
                              if report["me"]["person_id"] else "Set person_id for this environment in config.json.")
    return emit(report)


def cmd_find(p, cfg: dict, numbers: list[str]) -> int:
    try:
        queries = [parse_query(n) for n in numbers]
    except ValueError as exc:
        return emit({"status": "error", "error": str(exc)}, 1)
    with session(p, cfg, visible=False) as (context, mode, opened):
        page = new_page(context, cfg, mode, opened)
        err = open_board(page, cfg)
        if err:
            return emit({"status": "error", **err}, 1)
        results = search_cards(page, cfg, queries)
    return emit({"status": "ok", "environment": cfg["environment"], "browser_mode": mode, "results": results})


def cmd_history(p, cfg: dict, targets: list[str], days: int, today: str | None) -> int:
    ref = dt.date.fromisoformat(today) if today else dt.date.today()
    since = ref - dt.timedelta(days=days - 1)
    out = []
    with session(p, cfg, visible=False) as (context, mode, opened):
        page = new_page(context, cfg, mode, opened)
        resolved: list[dict] = []
        numbers = []
        for t in targets:
            g = GUID_RE.match(t.strip())
            if g:
                resolved.append({"query": t, "request_id": g.group(1)})
            else:
                try:
                    numbers.append(parse_query(t))
                except ValueError as exc:
                    out.append({"query": t, "status": "error", "error": str(exc)})
        if numbers:
            err = open_board(page, cfg)
            if err:
                return emit({"status": "error", **err}, 1)
            for r in search_cards(page, cfg, numbers):
                if r["decision"] == "unique":
                    m = r["matches"][0]
                    resolved.append({"query": r["query"], "request_id": m["request_id"],
                                     "request_number": m["request_number"], "description": m["description"]})
                else:
                    out.append({"query": r["query"], "status": r["decision"], "matches": r["matches"],
                                "error": r.get("error")})
        for item in resolved:
            got = read_card_history(page, cfg, item["request_id"])
            if got["status"] != "ok":
                out.append({**item, **got})
                continue
            state, entries = got["state"], got["entries"]
            by_date: dict[str, list] = {}
            for e in entries:
                if e["date"] and since.isoformat() <= e["date"] <= ref.isoformat():
                    by_date.setdefault(e["date"], []).append({k: e[k] for k in ("time", "author", "text")})
            dated = [e for e in entries if e["date"]]
            out.append({
                **item,
                "status": "ok",
                "title": state["title"],
                "field_editable": state["editable"],
                "auto_timestamp": state["auto_timestamp"],
                "total_entries": len(entries),
                "last_entry_date": max((e["date"] for e in dated), default=None),
                "today": ref.isoformat(),
                "today_logged": ref.isoformat() in by_date,
                "by_date": dict(sorted(by_date.items(), reverse=True)),
                "recent_texts": [e["text"] for e in entries[-5:]],
            })
    return emit({"status": "ok", "environment": cfg["environment"], "browser_mode": mode, "window_days": days,
                 "cards": out})


def git_evidence(cfg: dict, day: dt.date) -> dict:
    """Work items with git activity on `day` across the configured repos (commits and uncommitted work)."""
    from git_activity import repo_activity
    items: dict[str, dict] = {}
    errors = []
    for repo in cfg["work_log"]["repos"]:
        try:
            act = repo_activity(Path(repo), day, day, None, False)
        except Exception as exc:
            errors.append({"repo": repo, "error": str(exc)[:200]})
            continue
        name = Path(act["repo"]).name
        for wi, commits in act["by_day"].get(day.isoformat(), {}).items():
            if wi == "unlinked":
                continue
            e = items.setdefault(wi, {"work_item": wi, "commits": 0, "uncommitted_files": 0, "repos": [], "subjects": []})
            e["commits"] += len(commits)
            e["subjects"] += [c["subject"] for c in commits][:5]
            if name not in e["repos"]:
                e["repos"].append(name)
        touched_today = act["uncommitted"].get("modified_in_period_by_day", {}).get(day.isoformat(), 0)
        if touched_today:  # uncommitted files edited on this day, on a branch named after a work item
            for wi in act["current_branch_work_items"]:
                e = items.setdefault(wi, {"work_item": wi, "commits": 0, "uncommitted_files": 0, "repos": [], "subjects": []})
                e["uncommitted_files"] += touched_today
                if name not in e["repos"]:
                    e["repos"].append(name)
    return {"items": items, "errors": errors, "repos_scanned": len(cfg["work_log"]["repos"])}


def cmd_candidates(p, cfg: dict, date: str | None, max_history: int) -> int:
    day = dt.date.fromisoformat(date) if date else dt.date.today()
    git = git_evidence(cfg, day)
    cards: dict[str, dict] = {}
    with session(p, cfg, visible=False) as (context, mode, opened):
        page = new_page(context, cfg, mode, opened)
        err = open_board(page, cfg)
        if err:
            return emit({"status": "error", **err}, 1)
        me = whoami(page, cfg)
        # 1. cards for each work item seen in git today
        for wi, ev in git["items"].items():
            raw = board_query(page, cfg, wi)
            matches = classify(raw.get("items", []), {"number": int(wi), "kind": "any"}) if "error" not in raw else []
            for m in matches:
                c = cards.setdefault(m["request_id"], {**m, "work_items": [], "sources": [], "commits": 0,
                                                       "uncommitted_files": 0, "repos": []})
                c["work_items"].append(wi)
                c["sources"].append("git")
                c["commits"] += ev["commits"]
                c["uncommitted_files"] += ev["uncommitted_files"]
                c["repos"] += [r for r in ev["repos"] if r not in c["repos"]]
                c["ambiguous_work_item"] = len(matches) > 1
            if not matches:
                cards[f"wi-{wi}"] = {"request_number": None, "request_id": None, "description": "(no card found)",
                                     "status": "", "work_items": [wi], "sources": ["git"], "commits": ev["commits"],
                                     "uncommitted_files": ev["uncommitted_files"], "repos": ev["repos"]}
        # 2. your own active cards
        if me["person_id"]:
            raw = board_query(page, cfg, "", me["person_id"])
            for it in raw.get("items", []):
                if not is_active(it):
                    continue
                c = cards.setdefault(it["requestId"], {**card_summary(it), "work_items": [], "sources": [],
                                                       "commits": 0, "uncommitted_files": 0, "repos": []})
                if "my_active_card" not in c["sources"]:
                    c["sources"].append("my_active_card")
        # 3. rank, then read history for the top ones
        def rank(c):
            return (c["commits"] * 3 + min(c["uncommitted_files"], 10) * 0.5 + ("my_active_card" in c["sources"]))
        ordered = sorted(cards.values(), key=rank, reverse=True)
        for i, c in enumerate(ordered):
            c["rank"] = i + 1
            c["score"] = rank(c)
            if c.get("request_id") and i < max_history:
                got = read_card_history(page, cfg, c["request_id"])
                if got["status"] == "ok":
                    mine = [e for e in got["entries"] if e["date"] and (not me["name"] or e["author"] == me["name"])]
                    c["logged_today"] = any(e["date"] == day.isoformat() for e in mine)
                    c["last_entry_date"] = max((e["date"] for e in mine), default=None)
                    c["last_entry_excerpt"] = (mine[-1]["text"][:160] if mine else "")
                    c["field_editable"] = got["state"]["editable"]
                else:
                    c["history_error"] = got.get("error")
            c["recommended"] = bool(c.get("request_id")) and not c.get("logged_today", False) and (
                c["commits"] or c["uncommitted_files"] or "my_active_card" in c["sources"])
    return emit({"status": "ok", "environment": cfg["environment"], "browser_mode": mode, "date": day.isoformat(),
                 "me": me, "git": {"repos_scanned": git["repos_scanned"], "errors": git["errors"]},
                 "candidates": ordered})


def collect_entries(p, cfg: dict, since: dt.date, until: dt.date, extra_ids: list[str]) -> dict:
    """Your own Workflow remark entries between two dates, on your cards plus any extra request ids."""
    out_cards = []
    with session(p, cfg, visible=False) as (context, mode, opened):
        page = new_page(context, cfg, mode, opened)
        err = open_board(page, cfg)
        if err:
            return {"status": "error", **err}
        me = whoami(page, cfg)
        if not me["person_id"]:
            return {"status": "error", "error": "PersonID unknown: set person_id for this environment in config.json"}
        raw = board_query(page, cfg, "", me["person_id"])
        if "error" in raw:
            return {"status": "error", "error": raw["error"]}
        cards = {it["requestId"]: card_summary(it) for it in raw["items"]}
        for rid in extra_ids:
            cards.setdefault(rid, {"request_id": rid, "request_number": None, "description": "", "status": ""})
        for rid, card in cards.items():
            if card.get("start_date") and card["start_date"] > until.isoformat():
                continue  # started after the period: cannot hold entries inside it
            got = read_card_history(page, cfg, rid)
            if got["status"] != "ok":
                out_cards.append({**card, "error": got.get("error")})
                continue
            if not card.get("request_number"):
                m = re.search(r"(\d{2}\.\d{3}\.\d{3})", got["state"]["title"])
                card["request_number"] = m.group(1) if m else None
            mine = [e for e in got["entries"] if e["author"] == me["name"] and e["date"]
                    and since.isoformat() <= e["date"] <= until.isoformat()]
            if mine:
                out_cards.append({**card, "entries": mine})
    return {"status": "ok", "environment": cfg["environment"], "browser_mode": mode, "me": me,
            "since": since.isoformat(), "until": until.isoformat(), "cards": out_cards}


def cmd_entries(p, cfg: dict, since: str, until: str, extra: list[str]) -> int:
    res = collect_entries(p, cfg, dt.date.fromisoformat(since), dt.date.fromisoformat(until), extra)
    return emit(res, 0 if res["status"] == "ok" else 1)


def load_plan(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("cards", [])
    if not isinstance(data, list) or not data:
        raise ValueError("Plan must be a non-empty JSON list of {query, request_id, message}.")
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Plan item {i} is not an object.")
        g = GUID_RE.match(str(item.get("request_id", "")).strip())
        if not g:
            raise ValueError(f"Plan item {i} needs a request_id GUID (run `find` first).")
        item["request_id"] = g.group(1)
        msg = str(item.get("message", "")).strip()
        if not msg:
            raise ValueError(f"Plan item {i} has an empty message.")
        item["message"] = msg
    return data


def fill_one(page, cfg: dict, item: dict) -> dict:
    rep = {"query": item.get("query"), "request_id": item["request_id"]}
    err = goto_checked(page, request_url(cfg, item["request_id"]), cfg)
    if err:
        return {**rep, "status": "error", **err}
    state = read_state(page)
    rep["title"] = state["title"]
    if not state["has_field"]:
        return {**rep, "status": "skipped", "reason": "Remarks: Workflow field not on this request"}
    if not state["editable"]:
        return {**rep, "status": "skipped", "reason": "Remarks: Workflow is read-only for you on this request"}

    rx = stamp_regex(cfg["date_format"])
    ta = page.locator(REMARKS)
    ta.scroll_into_view_if_needed()
    ta.click()
    page.keyboard.press("Control+End")
    before = ta.input_value()
    page.keyboard.press("Enter")  # Synergy's auto-timestamp fires on the first key press
    added = ta.input_value()[len(before):]
    if rx.search(added):
        timestamp = "auto"
    else:
        for _ in range(len(ta.input_value()) - len(before)):
            page.keyboard.press("Backspace")
        if ta.input_value() != before:
            return {**rep, "status": "error", "reason": "could not undo the plain Enter before stamping; field left as typed"}
        if not state["has_timestamp_button"]:
            return {**rep, "status": "error", "reason": "no auto-timestamp and no Timestamp button found"}
        page.locator(TS_BUTTON).click()
        ta.focus()
        page.keyboard.press("Control+End")
        page.keyboard.press("Enter")
        added = ta.input_value()[len(before):]
        timestamp = "button" if rx.search(added) else "missing"
        if timestamp == "missing":
            return {**rep, "status": "error", "reason": "Timestamp button did not insert a timestamp"}
    page.keyboard.insert_text(item["message"])
    final = ta.input_value()
    ok = final.startswith(before) and final.endswith(item["message"])
    stamp = rx.search(added)
    return {**rep, "status": "filled" if ok else "error", "timestamp": timestamp,
            "timestamp_text": stamp.group(0) if stamp else None,
            "had_history": bool(before.strip()), "chars_typed": len(item["message"]),
            "reason": None if ok else "field content after typing did not match"}


def cmd_fill(p, cfg: dict, plan_path: str) -> int:
    try:
        plan = load_plan(plan_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return emit({"status": "error", "error": str(exc)}, 1)
    results = []
    filled = []
    with session(p, cfg, visible=True) as (context, mode, opened):
        already = {pg.url.lower() for pg in context.pages}
        for item in plan:
            guid = item["request_id"].lower()
            if any(guid in u for u in already):
                results.append({"query": item.get("query"), "request_id": item["request_id"], "status": "skipped",
                                "reason": "this card is already open in the automation window; save or close that tab first"})
                continue
            page = new_page(context, cfg, mode, opened)
            try:
                result = fill_one(page, cfg, item)
            except Exception as exc:  # report and continue with the next card
                result = {"query": item.get("query"), "request_id": item["request_id"], "status": "error",
                          "error": friendly_launch_error(exc)}
            results.append(result)
            if result["status"] == "filled":
                filled.append(page)
        if filled:
            try:
                filled[0].bring_to_front()
            except Exception:
                pass
    code = 0 if all(r["status"] == "filled" for r in results) else 1
    return emit({
        "status": "filled" if code == 0 else "partial",
        "environment": cfg["environment"],
        "browser_mode": mode,
        "saved": False,
        "next": "Review each tab in the Edge window and press Save yourself. Nothing was saved by the automation.",
        "results": results,
    }, code)


def main() -> int:
    parser = argparse.ArgumentParser(description="Exact Synergy automation for kanban-updater (never saves).")
    parser.add_argument("--env", help="environment block to use instead of the active one")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="pre-flight: settings, browser, portal and Kanban board")
    f = sub.add_parser("find", help="resolve numbers to Kanban cards")
    f.add_argument("numbers", nargs="+")
    h = sub.add_parser("history", help="read Workflow remark history")
    h.add_argument("targets", nargs="+", help="request GUIDs or numbers")
    h.add_argument("--days", type=int, default=30)
    h.add_argument("--today", help="reference date YYYY-MM-DD (default: today)")
    c = sub.add_parser("candidates", help="today's work items: git activity plus your active cards")
    c.add_argument("--date", help="day to collect, YYYY-MM-DD (default today)")
    c.add_argument("--max-history", type=int, default=12, help="read history for the top N candidates")
    e = sub.add_parser("entries", help="your own remark entries between two dates (input for points.py)")
    e.add_argument("--since", required=True)
    e.add_argument("--until", required=True)
    e.add_argument("--extra", nargs="*", default=[], help="extra request GUIDs to include")
    fl = sub.add_parser("fill", help="type remarks into cards in a visible window, without saving")
    fl.add_argument("--plan", required=True)
    args = parser.parse_args()

    try:
        cfg = load_config(env_override=args.env)
    except ConfigError as exc:
        return emit({"status": "error", "error": str(exc)}, 1)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return emit({"status": "error", "error": "playwright is not installed",
                     "hint": "python -m pip install playwright  (or run scripts/setup_environment.py --install)"}, 2)

    try:
        with sync_playwright() as p:
            if args.command == "check":
                return cmd_check(p, cfg)
            if args.command == "find":
                return cmd_find(p, cfg, args.numbers)
            if args.command == "history":
                return cmd_history(p, cfg, args.targets, max(1, args.days), args.today)
            if args.command == "candidates":
                return cmd_candidates(p, cfg, args.date, max(0, args.max_history))
            if args.command == "entries":
                return cmd_entries(p, cfg, args.since, args.until, args.extra)
            return cmd_fill(p, cfg, args.plan)
    except Exception as exc:
        return emit({"status": "error", "stage": args.command, "at": now_stamp(),
                     "error": friendly_launch_error(exc)}, 1)


if __name__ == "__main__":
    sys.exit(main())
