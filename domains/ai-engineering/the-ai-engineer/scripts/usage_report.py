#!/usr/bin/env python3
"""Cost, cache, latency, and error report from LLM call logs, using prices you supply.

Input: JSONL, one line per model call, exported from your own logs, traces, or provider
usage exports. Field names are configurable with --field NAME=dotted.path (defaults below),
or use --preset otel for OpenTelemetry GenAI attribute names.

  default fields: model, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens,
                  latency_ms, status, task_id, route, timestamp

Prices: a JSON file you fill in from each provider's current pricing page. The script never
invents prices. Units are per 1,000,000 tokens unless "per" is set:
  {"my-model": {"input": 3.0, "output": 15.0, "cache_read": 0.3, "cache_write": 3.75}}

Caching conventions differ by provider: some report cached tokens as part of input_tokens,
others report them separately. Pass --cached-in-input when input_tokens already includes
cache reads, so they are not billed twice.

Examples:
  python usage_report.py calls.jsonl --prices prices.json
  python usage_report.py calls.jsonl --prices prices.json --group route --top-tasks 10
  python usage_report.py spans.jsonl --preset otel --prices prices.json --json
  python usage_report.py calls.jsonl --field input_tokens=usage.prompt_tokens --field output_tokens=usage.completion_tokens --cached-in-input --field cache_read_tokens=usage.prompt_tokens_details.cached_tokens

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

DEFAULT_FIELDS = {
    "model": "model", "input_tokens": "input_tokens", "output_tokens": "output_tokens",
    "cache_read_tokens": "cache_read_tokens", "cache_write_tokens": "cache_write_tokens",
    "latency_ms": "latency_ms", "status": "status", "task_id": "task_id", "route": "route",
    "timestamp": "timestamp",
}
PRESETS = {
    "otel": {
        "model": "attributes.gen_ai.request.model",
        "input_tokens": "attributes.gen_ai.usage.input_tokens",
        "output_tokens": "attributes.gen_ai.usage.output_tokens",
        "status": "status.code",
        "task_id": "trace_id",
    },
}


def get_path(row: dict, path: str):
    """Dotted lookup that also accepts flat keys containing dots (common in OTel exports)."""
    if path in row:
        return row[path]
    node = row
    parts = path.split(".")
    i = 0
    while i < len(parts):
        if not isinstance(node, dict):
            return None
        for j in range(len(parts), i, -1):  # longest key first, so 'gen_ai.usage.input_tokens' works flat
            key = ".".join(parts[i:j])
            if key in node:
                node = node[key]
                i = j
                break
        else:
            return None
    return node


def num(value) -> float:
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def percentile(values: list[float], q: float):
    if not values:
        return None
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))]


def load_rows(path: str) -> list[dict]:
    rows = []
    with Path(path).open(encoding="utf-8-sig") as fh:
        for n, line in enumerate(fh, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    sys.exit(f"error: {path}:{n}: invalid JSON ({exc})")
    return rows


def cost_of(call: dict, prices: dict, cached_in_input: bool) -> float | None:
    price = prices.get(call["model"])
    if price is None:
        return None
    per = float(price.get("per", 1_000_000))
    uncached_input = call["input_tokens"] - (call["cache_read_tokens"] if cached_in_input else 0)
    return (max(0.0, uncached_input) * price.get("input", 0)
            + call["output_tokens"] * price.get("output", 0)
            + call["cache_read_tokens"] * price.get("cache_read", price.get("input", 0))
            + call["cache_write_tokens"] * price.get("cache_write", price.get("input", 0))) / per


def summarize(calls: list[dict], cached_in_input: bool) -> dict:
    n = len(calls)
    inp = sum(c["input_tokens"] for c in calls)
    out = sum(c["output_tokens"] for c in calls)
    cr = sum(c["cache_read_tokens"] for c in calls)
    cw = sum(c["cache_write_tokens"] for c in calls)
    total_prompt = inp if cached_in_input else inp + cr + cw
    costs = [c["cost"] for c in calls if c["cost"] is not None]
    lat = [c["latency_ms"] for c in calls if c["latency_ms"]]
    errors = sum(1 for c in calls if c["is_error"])
    return {
        "calls": n, "input_tokens": int(inp), "output_tokens": int(out),
        "cache_read_tokens": int(cr), "cache_write_tokens": int(cw),
        "cache_hit_rate": round(cr / total_prompt, 4) if total_prompt else None,
        "cost": round(sum(costs), 6) if costs else None,
        "unpriced_calls": n - len(costs),
        "avg_cost_per_call": round(sum(costs) / len(costs), 6) if costs else None,
        "latency_ms": {"p50": percentile(lat, 0.5), "p95": percentile(lat, 0.95), "p99": percentile(lat, 0.99)},
        "error_rate": round(errors / n, 4) if n else None,
    }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for field mapping and price format.")
    parser.add_argument("logs", help="JSONL file, one model call per line")
    parser.add_argument("--prices", help="JSON price table you filled from provider pricing pages")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="field-name preset")
    parser.add_argument("--field", action="append", default=[], metavar="NAME=PATH", help="override a field path")
    parser.add_argument("--cached-in-input", action="store_true",
                        help="input_tokens already includes cache-read tokens (do not bill them twice)")
    parser.add_argument("--group", choices=("model", "route"), default="model", help="breakdown key")
    parser.add_argument("--top-tasks", type=int, default=5, help="show the N most expensive tasks (needs task_id)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    fields = dict(DEFAULT_FIELDS)
    if args.preset:
        fields.update(PRESETS[args.preset])
    for item in args.field:
        name, _, path = item.partition("=")
        if name not in DEFAULT_FIELDS or not path:
            sys.exit(f"error: --field must be NAME=PATH with NAME in {sorted(DEFAULT_FIELDS)}")
        fields[name] = path
    prices = json.loads(Path(args.prices).read_text(encoding="utf-8")) if args.prices else {}

    calls = []
    for row in load_rows(args.logs):
        status = get_path(row, fields["status"])
        call = {
            "model": str(get_path(row, fields["model"]) or "(unknown)"),
            "input_tokens": num(get_path(row, fields["input_tokens"])),
            "output_tokens": num(get_path(row, fields["output_tokens"])),
            "cache_read_tokens": num(get_path(row, fields["cache_read_tokens"])),
            "cache_write_tokens": num(get_path(row, fields["cache_write_tokens"])),
            "latency_ms": num(get_path(row, fields["latency_ms"])),
            "task_id": get_path(row, fields["task_id"]),
            "route": str(get_path(row, fields["route"]) or "(none)"),
            "is_error": status is not None and str(status).lower() in {"error", "failed", "2", "status_code_error", "timeout"},
        }
        call["cost"] = cost_of(call, prices, args.cached_in_input)
        calls.append(call)
    if not calls:
        sys.exit("error: no calls in the log")

    groups: dict[str, list[dict]] = {}
    for c in calls:
        groups.setdefault(c[args.group], []).append(c)
    tasks: dict[str, list[dict]] = {}
    for c in calls:
        if c["task_id"] is not None:
            tasks.setdefault(str(c["task_id"]), []).append(c)
    task_costs = {t: sum(c["cost"] or 0 for c in cs) for t, cs in tasks.items()}
    report = {
        "overall": summarize(calls, args.cached_in_input),
        f"by_{args.group}": {k: summarize(v, args.cached_in_input) for k, v in sorted(groups.items())},
        "tasks": {
            "count": len(tasks),
            "avg_calls_per_task": round(sum(len(v) for v in tasks.values()) / len(tasks), 2) if tasks else None,
            "avg_cost_per_task": round(sum(task_costs.values()) / len(tasks), 6) if tasks and prices else None,
            "most_expensive": [{"task_id": t, "cost": round(c, 6), "calls": len(tasks[t])}
                               for t, c in sorted(task_costs.items(), key=lambda kv: -kv[1])[: args.top_tasks]]
            if prices else [],
        },
        "unpriced_models": sorted({c["model"] for c in calls if c["cost"] is None}) if prices else [],
        "notes": [],
    }
    if not prices:
        report["notes"].append("No --prices given: tokens and latency only. Fill a price table from provider docs.")
    if report["unpriced_models"]:
        report["notes"].append(f"No price for: {', '.join(report['unpriced_models'])}")
    if report["overall"]["cache_read_tokens"] == 0:
        report["notes"].append("No cache reads recorded: either caching is off, prompts lack a stable prefix, "
                               "or the cache field is not mapped (--field cache_read_tokens=...).")

    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    o = report["overall"]
    print(f"{o['calls']} calls | input {o['input_tokens']:,} | output {o['output_tokens']:,} | "
          f"cache read {o['cache_read_tokens']:,} | cache write {o['cache_write_tokens']:,}")
    if o["cost"] is not None:
        print(f"Cost: {o['cost']:.4f} (avg {o['avg_cost_per_call']:.6f}/call; {o['unpriced_calls']} unpriced call(s))")
    if o["cache_hit_rate"] is not None:
        print(f"Cache hit rate: {o['cache_hit_rate']:.1%} of prompt tokens")
    lat = o["latency_ms"]
    if lat["p50"] is not None:
        print(f"Latency ms: p50 {lat['p50']:.0f} | p95 {lat['p95']:.0f} | p99 {lat['p99']:.0f}")
    print(f"Error rate: {o['error_rate']:.1%}")
    print(f"\nBy {args.group}:")
    for key, s in report[f"by_{args.group}"].items():
        cost = f"{s['cost']:.4f}" if s["cost"] is not None else "n/a"
        hit = f"{s['cache_hit_rate']:.0%}" if s["cache_hit_rate"] is not None else "n/a"
        p95 = f"{s['latency_ms']['p95']:.0f} ms" if s["latency_ms"]["p95"] is not None else "n/a"
        print(f"  {key}: {s['calls']} calls, cost {cost}, cache {hit}, p95 {p95}, errors {s['error_rate']:.0%}")
    t = report["tasks"]
    if t["count"]:
        print(f"\nTasks: {t['count']} ({t['avg_calls_per_task']} calls/task"
              + (f", {t['avg_cost_per_task']:.6f}/task)" if t["avg_cost_per_task"] is not None else ")"))
        for item in t["most_expensive"]:
            print(f"  {item['task_id']}: {item['cost']:.4f} over {item['calls']} call(s)")
    for note in report["notes"]:
        print(f"Note: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
