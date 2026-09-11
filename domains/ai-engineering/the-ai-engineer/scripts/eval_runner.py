#!/usr/bin/env python3
"""Provider-neutral eval harness for LLM features: run a dataset through any target, grade, compare runs.

Targets (how the system under test is called for each case):
  --target-cmd "python app.py"     case input is sent as JSON on stdin; stdout is the output
                                   (if stdout is a JSON object with an "output" key, "usage" and
                                   "trajectory" are recorded too)
  --target-py  app.module:function function(input) returns a string or {"output": ..., "usage": {...}}
  --oracle                         uses each case's "expected" as the output (grader sanity check)
  --null                           uses an empty output (graders must fail it)

Dataset: JSONL, one case per line:
  {"id": "refund-1", "input": "...", "expected": "...", "tags": ["policy"],
   "graders": [{"type": "contains", "value": "30 days"}], "aggregate": "all"}
Graders missing from a case come from --graders FILE (a JSON list).

Grader types: exact, contains, not_contains, regex, one_of, numeric, json_valid, json_schema,
json_path, max_length, retrieval_recall, python (module:function for custom or LLM-judge graders).

Commands:
  validate --dataset cases.jsonl [--graders g.json]
  run      --dataset cases.jsonl (--target-cmd CMD | --target-py MOD:FN | --oracle | --null)
           [--reps 3] [--concurrency 4] [--timeout 120] [--retries 2] [--out runs/NAME]
  compare  --baseline runs/A --candidate runs/B [--fail-on-regression]

Results: results.jsonl (graded attempts), errors.jsonl (attempts that never produced output:
timeouts, crashes, non-zero exits; never scored as failures), summary.json.

Standard library only.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime as dt
import hashlib
import importlib
import json
import math
import random
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

GRADER_TYPES = {"exact", "contains", "not_contains", "regex", "one_of", "numeric", "json_valid",
                "json_schema", "json_path", "max_length", "retrieval_recall", "python"}
NUMBER_RE = re.compile(r"-?\d+(?:[.,]\d+)*(?:\.\d+)?")


class HarnessError(Exception):
    """An attempt that produced no gradable output (not a model failure)."""


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"error: {path}:{n}: invalid JSON ({exc})")
            if not isinstance(row, dict):
                raise SystemExit(f"error: {path}:{n}: each line must be a JSON object")
            rows.append(row)
    return rows


def load_cases(dataset: str, graders_file: str | None) -> tuple[list[dict], list[str]]:
    cases = load_jsonl(Path(dataset))
    default_graders = json.loads(Path(graders_file).read_text(encoding="utf-8")) if graders_file else []
    problems, seen = [], set()
    for i, case in enumerate(cases, 1):
        cid = case.get("id")
        if not isinstance(cid, str) or not cid:
            problems.append(f"case #{i}: missing string 'id'")
            case["id"] = f"case-{i}"
        elif cid in seen:
            problems.append(f"case {cid}: duplicate id")
        seen.add(case["id"])
        if "input" not in case:
            problems.append(f"case {case['id']}: missing 'input'")
        case.setdefault("graders", default_graders)
        if not case["graders"]:
            problems.append(f"case {case['id']}: no graders (add 'graders' or pass --graders)")
        for g in case["graders"]:
            if not isinstance(g, dict) or g.get("type") not in GRADER_TYPES:
                problems.append(f"case {case['id']}: unknown grader {g!r}")
        if case.get("aggregate", "all") not in ("all", "any"):
            problems.append(f"case {case['id']}: aggregate must be 'all' or 'any'")
    return cases, problems


# ---------------------------------------------------------------------------
# Graders
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def as_text(output) -> str:
    return output if isinstance(output, str) else json.dumps(output, ensure_ascii=False)


def parse_json(output):
    if not isinstance(output, str):
        return output
    text = output.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    return json.loads(text)


def schema_errors(value, schema: dict, path: str = "$") -> list[str]:
    """Minimal JSON Schema subset: type, enum, const, required, properties,
    additionalProperties, items, minItems, maxItems, minLength, maxLength, minimum, maximum."""
    errors: list[str] = []
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    expected = schema.get("type")
    if expected:
        allowed = expected if isinstance(expected, list) else [expected]

        def matches(t: str) -> bool:
            if t == "integer":
                return isinstance(value, int) and not isinstance(value, bool)
            if t == "number":
                return isinstance(value, (int, float)) and not isinstance(value, bool)
            return isinstance(value, types.get(t, object))

        if not any(matches(t) for t in allowed):
            return [f"{path}: expected {expected}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required '{key}'")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in value:
                errors += schema_errors(value[key], sub, f"{path}.{key}")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(props))
            if extra:
                errors.append(f"{path}: unexpected properties {extra}")
    if isinstance(value, list):
        if "items" in schema:
            for i, item in enumerate(value):
                errors += schema_errors(item, schema["items"], f"{path}[{i}]")
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than {schema['maxItems']} items")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    return errors


def json_path_get(data, path: str):
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if part.startswith("["):
            data = data[int(part[1:-1])]
        else:
            data = data[part]
    return data


def load_callable(spec: str, search_paths: list[str]):
    module_name, _, func_name = spec.partition(":")
    if not func_name:
        raise SystemExit(f"error: '{spec}' must look like module:function")
    for p in search_paths:
        if p not in sys.path:
            sys.path.insert(0, p)
    return getattr(importlib.import_module(module_name), func_name)


def grade_one(grader: dict, output, case: dict, search_paths: list[str]) -> dict:
    kind = grader["type"]
    name = grader.get("name", kind)
    text = as_text(output)
    try:
        if kind == "exact":
            target = grader.get("value", case.get("expected"))
            ok = normalize(text) == normalize(as_text(target)) if grader.get("normalize", True) else text == as_text(target)
            return {"name": name, "pass": ok, "reason": "" if ok else "output differs from expected"}
        if kind in ("contains", "not_contains"):
            values = grader.get("values") or [grader.get("value", case.get("expected"))]
            hay = normalize(text) if grader.get("normalize", True) else text
            found = [v for v in values if (normalize(as_text(v)) if grader.get("normalize", True) else as_text(v)) in hay]
            ok = len(found) == len(values) if kind == "contains" else not found
            missing = [v for v in values if v not in found]
            return {"name": name, "pass": ok,
                    "reason": "" if ok else (f"missing {missing}" if kind == "contains" else f"found forbidden {found}")}
        if kind == "regex":
            flags = re.I if grader.get("ignore_case", True) else 0
            ok = re.search(grader["pattern"], text, flags | re.S) is not None
            return {"name": name, "pass": ok, "reason": "" if ok else f"no match for /{grader['pattern']}/"}
        if kind == "one_of":
            ok = normalize(text) in {normalize(as_text(v)) for v in grader["values"]}
            return {"name": name, "pass": ok, "reason": "" if ok else "not one of the allowed values"}
        if kind == "numeric":
            target = float(grader.get("value", case.get("expected")))
            numbers = NUMBER_RE.findall(text)
            if not numbers:
                return {"name": name, "pass": False, "reason": "no number in output"}
            got = float(numbers[0].replace(",", ""))
            tol = grader.get("tolerance", 0.0)
            if grader.get("relative"):
                tol = abs(target) * tol
            ok = abs(got - target) <= tol
            return {"name": name, "pass": ok, "score": got, "reason": "" if ok else f"{got} vs {target} (tol {tol})"}
        if kind == "max_length":
            ok = len(text) <= grader["value"]
            return {"name": name, "pass": ok, "reason": "" if ok else f"{len(text)} chars > {grader['value']}"}
        if kind in ("json_valid", "json_schema", "json_path"):
            try:
                data = parse_json(output)
            except (json.JSONDecodeError, TypeError) as exc:
                return {"name": name, "pass": False, "reason": f"invalid JSON: {exc}"}
            if kind == "json_valid":
                return {"name": name, "pass": True, "reason": ""}
            if kind == "json_schema":
                errs = schema_errors(data, grader["schema"])
                return {"name": name, "pass": not errs, "reason": "; ".join(errs[:5])}
            try:
                got = json_path_get(data, grader["path"])
            except (KeyError, IndexError, TypeError):
                return {"name": name, "pass": False, "reason": f"path {grader['path']} not found"}
            want = grader.get("value", case.get("expected"))
            ok = normalize(as_text(got)) == normalize(as_text(want)) if isinstance(got, str) else got == want
            return {"name": name, "pass": ok, "reason": "" if ok else f"{grader['path']} = {got!r}, expected {want!r}"}
        if kind == "retrieval_recall":
            try:
                data = parse_json(output)
            except (json.JSONDecodeError, TypeError):
                return {"name": name, "pass": False, "reason": "output is not a JSON list of ids"}
            retrieved = data.get("retrieved", []) if isinstance(data, dict) else data
            k = grader.get("k", len(retrieved))
            relevant = set(grader.get("relevant", case.get("expected") or []))
            if not relevant:
                return {"name": name, "pass": False, "reason": "no relevant ids given"}
            recall = len(relevant & set(retrieved[:k])) / len(relevant)
            ok = recall >= grader.get("threshold", 1.0)
            return {"name": name, "pass": ok, "score": round(recall, 4), "reason": "" if ok else f"recall@{k} = {recall:.2f}"}
        if kind == "python":
            fn = load_callable(grader["function"], search_paths)
            result = fn(output, case)
            if isinstance(result, bool):
                return {"name": name, "pass": result, "reason": ""}
            if isinstance(result, dict) and "pass" in result:
                return {"name": name, "pass": bool(result["pass"]), "score": result.get("score"),
                        "reason": str(result.get("reason", ""))}
            raise HarnessError(f"python grader {grader['function']} must return bool or {{'pass': ...}}")
    except HarnessError:
        raise
    except Exception as exc:  # a crashing grader is a harness problem, not a model failure
        raise HarnessError(f"grader {name} crashed: {type(exc).__name__}: {exc}")
    raise HarnessError(f"unknown grader type {kind}")


def grade(case: dict, output, search_paths: list[str]) -> tuple[bool, list[dict]]:
    results = [grade_one(g, output, case, search_paths) for g in case["graders"]]
    combine = all if case.get("aggregate", "all") == "all" else any
    return combine(r["pass"] for r in results), results


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------

def make_target(args):
    if args.oracle:
        return lambda case: {"output": case.get("expected", "")}
    if args.null:
        return lambda case: {"output": ""}
    if args.target_py:
        fn = load_callable(args.target_py, [args.path])

        def call_py(case):
            result = fn(case["input"])
            return result if isinstance(result, dict) and "output" in result else {"output": result}
        return call_py
    if args.target_cmd:
        def call_cmd(case):
            try:
                proc = subprocess.run(args.target_cmd, shell=True, input=json.dumps(case["input"], ensure_ascii=False),
                                      capture_output=True, text=True, encoding="utf-8", timeout=args.timeout,
                                      cwd=args.path)
            except subprocess.TimeoutExpired:
                raise HarnessError(f"timeout after {args.timeout}s")
            if proc.returncode != 0:
                raise HarnessError(f"exit code {proc.returncode}: {proc.stderr.strip()[-500:]}")
            out = proc.stdout.strip()
            try:
                parsed = json.loads(out)
                if isinstance(parsed, dict) and "output" in parsed:
                    return parsed
            except json.JSONDecodeError:
                pass
            return {"output": out}
        return call_cmd
    raise SystemExit("error: choose a target: --target-cmd, --target-py, --oracle, or --null")


def attempt(case: dict, rep: int, target, args, search_paths: list[str]) -> tuple[str, dict]:
    last_error = ""
    for n in range(args.retries + 1):
        start = time.perf_counter()
        try:
            result = target(case)
            latency = time.perf_counter() - start
            passed, grades = grade(case, result.get("output"), search_paths)
            row = {
                "case_id": case["id"], "rep": rep, "pass": passed, "grades": grades,
                "output": result.get("output"), "latency_s": round(latency, 3), "attempts": n + 1,
                "tags": case.get("tags", []),
            }
            for key in ("usage", "model", "trajectory", "stop_reason", "status"):
                if key in result:
                    row[key] = result[key]
            return "result", row
        except HarnessError as exc:
            last_error = str(exc)
        except Exception as exc:  # target crashed
            last_error = f"{type(exc).__name__}: {exc}"
        if n < args.retries:
            time.sleep(min(30, (2 ** n) + random.random()))  # jittered backoff
    return "error", {"case_id": case["id"], "rep": rep, "error": last_error, "attempts": args.retries + 1}


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def wilson(passes: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = passes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return ordered[idx]


def per_case_means(results: list[dict]) -> dict[str, float]:
    buckets: dict[str, list[int]] = {}
    for r in results:
        buckets.setdefault(r["case_id"], []).append(1 if r["pass"] else 0)
    return {cid: sum(v) / len(v) for cid, v in buckets.items()}


def summarize(results: list[dict], errors: list[dict], cases: list[dict], meta: dict) -> dict:
    means = per_case_means(results)
    n_attempts = len(results)
    passes = sum(1 for r in results if r["pass"])
    lo, hi = wilson(passes, n_attempts)
    tags: dict[str, list[float]] = {}
    for case in cases:
        if case["id"] in means:
            for tag in case.get("tags", []) or ["(untagged)"]:
                tags.setdefault(tag, []).append(means[case["id"]])
    graders: dict[str, list[int]] = {}
    for r in results:
        for g in r["grades"]:
            graders.setdefault(g["name"], []).append(1 if g["pass"] else 0)
    latencies = [r["latency_s"] for r in results]
    usage_totals: dict[str, float] = {}
    for r in results:
        for k, v in (r.get("usage") or {}).items():
            if isinstance(v, (int, float)):
                usage_totals[k] = usage_totals.get(k, 0) + v
    flaky = [cid for cid, m in means.items() if 0 < m < 1]
    return {
        **meta,
        "cases": len(cases), "cases_scored": len(means), "attempts_scored": n_attempts, "attempts_errored": len(errors),
        "pass_rate": round(passes / n_attempts, 4) if n_attempts else None,
        "pass_rate_ci95": [round(lo, 4), round(hi, 4)],
        "noise_floor_hint": round(1 / math.sqrt(n_attempts), 3) if n_attempts else None,
        "by_tag": {t: {"cases": len(v), "pass_rate": round(sum(v) / len(v), 4)} for t, v in sorted(tags.items())},
        "by_grader": {g: round(sum(v) / len(v), 4) for g, v in sorted(graders.items())},
        "flaky_cases": sorted(flaky),
        "latency_s": {"p50": percentile(latencies, 0.5), "p95": percentile(latencies, 0.95)},
        "usage_totals": usage_totals,
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_validate(args) -> int:
    cases, problems = load_cases(args.dataset, args.graders)
    inputs = [json.dumps(c.get("input"), sort_keys=True) for c in cases]
    dupes = len(inputs) - len(set(inputs))
    tags: dict[str, int] = {}
    for c in cases:
        for t in c.get("tags", []) or ["(untagged)"]:
            tags[t] = tags.get(t, 0) + 1
    print(f"{len(cases)} cases; {dupes} duplicate input(s); tags: {tags}")
    for p in problems:
        print(f"  ERROR {p}")
    if len(cases) < 20:
        print("  note: fewer than 20 cases gives a wide confidence interval; see references/evals.md")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_run(args) -> int:
    cases, problems = load_cases(args.dataset, args.graders)
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        return 2
    if args.limit:
        cases = cases[: args.limit]
    target = make_target(args)
    label = "oracle" if args.oracle else "null" if args.null else (args.target_py or args.target_cmd)
    out_dir = Path(args.out or f"runs/{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}")
    out_dir.mkdir(parents=True, exist_ok=True)
    dataset_hash = hashlib.sha256(Path(args.dataset).read_bytes()).hexdigest()[:16]
    meta = {"target": label, "dataset": args.dataset, "dataset_sha256_16": dataset_hash, "reps": args.reps,
            "started_at": dt.datetime.now().isoformat(timespec="seconds"), "note": args.note or ""}
    search_paths = [args.path]
    jobs = [(case, rep) for case in cases for rep in range(args.reps)]
    results, errors = [], []
    with futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        pending = {pool.submit(attempt, case, rep, target, args, search_paths): (case["id"], rep) for case, rep in jobs}
        for done, fut in enumerate(futures.as_completed(pending), 1):
            kind, row = fut.result()
            (results if kind == "result" else errors).append(row)
            if not args.quiet and (done % 10 == 0 or done == len(jobs)):
                print(f"  {done}/{len(jobs)} attempts", file=sys.stderr)
    results.sort(key=lambda r: (r["case_id"], r["rep"]))
    errors.sort(key=lambda r: (r["case_id"], r["rep"]))
    with (out_dir / "results.jsonl").open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (out_dir / "errors.jsonl").open("w", encoding="utf-8") as fh:
        for r in errors:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = summarize(results, errors, cases, meta)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Run: {label} on {len(cases)} cases x {args.reps} rep(s) -> {out_dir}")
    if summary["pass_rate"] is not None:
        lo, hi = summary["pass_rate_ci95"]
        print(f"Pass rate: {summary['pass_rate']:.1%}  (95% CI {lo:.1%}-{hi:.1%}, {summary['attempts_scored']} scored attempts)")
    print(f"Errored attempts (not scored): {len(errors)}")
    if jobs and len(errors) / len(jobs) > 0.1:
        print(f"WARNING: {len(errors)}/{len(jobs)} attempts errored; the pass rate describes only the attempts that "
              "completed and may be biased. Fix the harness or retry before drawing conclusions (see errors.jsonl).")
    for tag, info in summary["by_tag"].items():
        print(f"  tag {tag}: {info['pass_rate']:.1%} over {info['cases']} case(s)")
    for g, rate in summary["by_grader"].items():
        print(f"  grader {g}: {rate:.1%}")
    if summary["flaky_cases"]:
        print(f"Flaky cases (pass on some reps only): {', '.join(summary['flaky_cases'][:10])}")
    failed = sorted({r["case_id"] for r in results if not r["pass"]})
    if failed:
        print(f"Failing cases: {', '.join(failed[:15])}{' ...' if len(failed) > 15 else ''}")
    if args.oracle and failed:
        print("WARNING: oracle run failed some cases: the reference answers or graders are wrong.")
    if args.null and summary["pass_rate"]:
        print("WARNING: null run passed some cases: those graders are too lenient.")
    return 0


def load_run(run_dir: str) -> tuple[list[dict], dict]:
    path = Path(run_dir)
    results = load_jsonl(path / "results.jsonl")
    summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
    return results, summary


def cmd_compare(args) -> int:
    base_results, base_summary = load_run(args.baseline)
    cand_results, cand_summary = load_run(args.candidate)
    if base_summary.get("dataset_sha256_16") != cand_summary.get("dataset_sha256_16"):
        print("WARNING: the runs used different dataset files; the comparison may be meaningless.")
    base, cand = per_case_means(base_results), per_case_means(cand_results)
    shared = sorted(set(base) & set(cand))
    if not shared:
        print("error: no cases in common", file=sys.stderr)
        return 2
    diffs = [cand[c] - base[c] for c in shared]
    mean_diff = statistics.fmean(diffs)
    rng = random.Random(args.seed)
    boots = []
    for _ in range(args.bootstrap):
        sample = [diffs[rng.randrange(len(diffs))] for _ in diffs]
        boots.append(statistics.fmean(sample))
    boots.sort()
    lo = boots[int(0.025 * len(boots))]
    hi = boots[int(0.975 * len(boots)) - 1]
    regressions = [c for c in shared if cand[c] < base[c]]
    fixes = [c for c in shared if cand[c] > base[c]]
    base_rate = statistics.fmean(base[c] for c in shared)
    cand_rate = statistics.fmean(cand[c] for c in shared)
    verdict = ("better" if lo > 0 else "worse" if hi < 0 else "no significant difference")
    report = {
        "cases_compared": len(shared), "baseline_pass_rate": round(base_rate, 4), "candidate_pass_rate": round(cand_rate, 4),
        "mean_difference": round(mean_diff, 4), "difference_ci95": [round(lo, 4), round(hi, 4)], "verdict": verdict,
        "regressions": regressions, "fixes": fixes,
        "only_in_baseline": sorted(set(base) - set(cand)), "only_in_candidate": sorted(set(cand) - set(base)),
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Compared {len(shared)} shared cases (paired, bootstrap {args.bootstrap}x)")
        print(f"  baseline  {base_rate:.1%}   ({args.baseline})")
        print(f"  candidate {cand_rate:.1%}   ({args.candidate})")
        print(f"  difference {mean_diff:+.1%}  (95% CI {lo:+.1%} to {hi:+.1%}) -> {verdict}")
        print(f"  regressions ({len(regressions)}): {', '.join(regressions[:15]) or '-'}")
        print(f"  fixes ({len(fixes)}): {', '.join(fixes[:15]) or '-'}")
        for key in ("only_in_baseline", "only_in_candidate"):
            if report[key]:
                print(f"  {key.replace('_', ' ')}: {len(report[key])} case(s)")
    if args.fail_on_regression and (verdict == "worse" or (args.must_pass_tag and any(
            args.must_pass_tag in r.get("tags", []) and not r["pass"] for r in cand_results))):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for dataset and grader formats.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="check a dataset")
    p.add_argument("--dataset", required=True)
    p.add_argument("--graders", help="JSON list of default graders")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("run", help="run a dataset through a target and grade it")
    p.add_argument("--dataset", required=True)
    p.add_argument("--graders", help="JSON list of default graders")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--target-cmd", help="shell command; case input as JSON on stdin")
    target.add_argument("--target-py", help="module:function called with the case input")
    target.add_argument("--oracle", action="store_true", help="use each case's expected value (grader check)")
    target.add_argument("--null", action="store_true", help="use an empty output (graders must fail)")
    p.add_argument("--path", default=".", help="working directory / import path for targets and python graders")
    p.add_argument("--reps", type=int, default=1, help="repetitions per case (use 3+ for decisions)")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--timeout", type=int, default=120, help="seconds per target call (--target-cmd)")
    p.add_argument("--retries", type=int, default=2, help="retries for harness errors, with jittered backoff")
    p.add_argument("--limit", type=int, help="only the first N cases (smoke test)")
    p.add_argument("--out", help="run directory (default runs/<timestamp>)")
    p.add_argument("--note", help="free-text note stored in summary.json (e.g. prompt version)")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("compare", help="paired comparison of two runs")
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--fail-on-regression", action="store_true", help="exit 1 if significantly worse (for CI)")
    p.add_argument("--must-pass-tag", help="with --fail-on-regression: also fail if any case with this tag fails")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_compare)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
