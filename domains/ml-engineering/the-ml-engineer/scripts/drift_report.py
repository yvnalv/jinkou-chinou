#!/usr/bin/env python3
"""Compare a current data window with a reference (training) window: schema changes, data quality,
feature drift, and prediction drift.

Per column:
  numeric      PSI on reference-quantile bins, Kolmogorov-Smirnov statistic, mean and std shift,
               share outside the reference range, missing-rate change
  categorical  PSI over categories, share of unseen categories, missing-rate change
Schema: missing columns, new columns, and type changes.

PSI bands (rule of thumb): < 0.1 stable, 0.1-0.25 moderate, > 0.25 major.
Drift is a signal to investigate, not proof that the model got worse: confirm with labelled
performance when labels arrive.

Examples:
  python drift_report.py --reference train.parquet --current prod_2026-09.parquet
  python drift_report.py --reference train.csv --current last_week.csv --exclude customer_id --prediction-col score --out drift.json

Exit code 1 when any column (or the prediction column) shows major drift or the schema changed.
Requires pandas and numpy.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.exit("drift_report.py needs pandas and numpy: pip install pandas numpy")


def read_any(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.is_file():
        sys.exit(f"error: file not found: {path}")
    if p.suffix.lower() in (".parquet", ".pq"):
        return pd.read_parquet(p)
    if p.suffix.lower() in (".jsonl", ".ndjson"):
        return pd.read_json(p, lines=True)
    return pd.read_csv(p, low_memory=False)


def band(psi: float | None) -> str:
    if psi is None:
        return "n/a"
    return "stable" if psi < 0.1 else "moderate" if psi < 0.25 else "major"


def psi_numeric(ref: np.ndarray, cur: np.ndarray, bins: int) -> float | None:
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return None
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.clip(np.histogram(ref, edges)[0] / len(ref), 1e-4, None)
    c = np.clip(np.histogram(cur, edges)[0] / len(cur), 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))


def ks_statistic(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.sort(a), np.sort(b)
    values = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, values, side="right") / len(a)
    cdf_b = np.searchsorted(b, values, side="right") / len(b)
    return float(np.max(np.abs(cdf_a - cdf_b)))


def numeric_drift(ref: pd.Series, cur: pd.Series, bins: int) -> dict:
    r, c = ref.dropna().astype(float).to_numpy(), cur.dropna().astype(float).to_numpy()
    out = {"type": "numeric", "missing_ref": round(float(ref.isna().mean()), 4), "missing_cur": round(float(cur.isna().mean()), 4)}
    if len(r) == 0 or len(c) == 0:
        out["psi"] = None
        return out
    sd = float(np.std(r)) or 1.0
    out.update({
        "psi": round(psi_numeric(r, c, bins), 4) if psi_numeric(r, c, bins) is not None else None,
        "ks": round(ks_statistic(r, c), 4),
        "mean_ref": round(float(np.mean(r)), 4), "mean_cur": round(float(np.mean(c)), 4),
        "mean_shift_in_sd": round((float(np.mean(c)) - float(np.mean(r))) / sd, 3),
        "std_ratio": round(float(np.std(c)) / sd, 3),
        "outside_ref_range": round(float(((c < r.min()) | (c > r.max())).mean()), 4),
    })
    return out


def categorical_drift(ref: pd.Series, cur: pd.Series, top: int = 50) -> dict:
    r, c = ref.dropna().astype(str), cur.dropna().astype(str)
    out = {"type": "categorical", "missing_ref": round(float(ref.isna().mean()), 4), "missing_cur": round(float(cur.isna().mean()), 4)}
    if r.empty or c.empty:
        out["psi"] = None
        return out
    keep = r.value_counts().index[:top]
    rp = r.where(r.isin(keep), "__other__").value_counts(normalize=True)
    cp = c.where(c.isin(keep) | ~c.isin(set(r)), "__other__")
    unseen = ~cp.isin(set(r)) & (cp != "__other__")
    cp = cp.where(~unseen, "__unseen__").value_counts(normalize=True)
    cats = rp.index.union(cp.index)
    a = np.clip(rp.reindex(cats, fill_value=0).to_numpy(), 1e-4, None)
    b = np.clip(cp.reindex(cats, fill_value=0).to_numpy(), 1e-4, None)
    shares = (cp - rp.reindex(cp.index, fill_value=0)).sort_values(key=np.abs, ascending=False)
    out.update({
        "psi": round(float(np.sum((b - a) * np.log(b / a))), 4),
        "unseen_share": round(float(unseen.mean()), 4),
        "unseen_examples": sorted(c[~c.isin(set(r))].unique()[:5].tolist()),
        "largest_share_changes": {k: round(float(v), 4) for k, v in shares.head(3).items()},
    })
    return out


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for metrics and thresholds.")
    parser.add_argument("--reference", required=True, help="reference window (usually training or validation data)")
    parser.add_argument("--current", required=True, help="current window (recent production inputs)")
    parser.add_argument("--columns", help="comma list of columns to check (default: all shared)")
    parser.add_argument("--exclude", default="", help="comma list of columns to skip (IDs, timestamps)")
    parser.add_argument("--prediction-col", help="model output column present in both windows")
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--missing-change", type=float, default=0.05, help="flag missing-rate increases above this")
    parser.add_argument("--out", help="write JSON report")
    args = parser.parse_args(argv)

    ref, cur = read_any(args.reference), read_any(args.current)
    excluded = {c for c in args.exclude.split(",") if c}
    if args.columns:  # only the requested columns matter (e.g. model features inside a prediction log)
        wanted = [c for c in args.columns.split(",") if c and c not in excluded]
        schema = {"missing_in_current": sorted(c for c in wanted if c in ref.columns and c not in cur.columns),
                  "missing_in_reference": sorted(c for c in wanted if c not in ref.columns),
                  "new_in_current": [], "type_changes": {}}
        shared = [c for c in wanted if c in ref.columns and c in cur.columns]
    else:
        schema = {
            "missing_in_current": sorted(set(ref.columns) - set(cur.columns) - excluded),
            "new_in_current": sorted(set(cur.columns) - set(ref.columns) - excluded),
            "type_changes": {},
        }
        shared = [c for c in ref.columns if c in cur.columns and c not in excluded]
    for col in shared:
        num_ref, num_cur = pd.api.types.is_numeric_dtype(ref[col]), pd.api.types.is_numeric_dtype(cur[col])
        if num_ref != num_cur:
            schema["type_changes"][col] = f"{ref[col].dtype} -> {cur[col].dtype}"

    columns = {}
    flags = []
    for col in shared:
        if col in schema["type_changes"]:
            continue
        is_num = pd.api.types.is_numeric_dtype(ref[col]) and ref[col].nunique() > 10
        info = numeric_drift(ref[col], cur[col], args.bins) if is_num else categorical_drift(ref[col], cur[col])
        info["band"] = band(info.get("psi"))
        columns[col] = info
        role = "prediction" if col == args.prediction_col else "feature"
        if info["band"] == "major":
            flags.append(("major", col, f"{role} PSI {info['psi']}"))
        elif info["band"] == "moderate":
            flags.append(("moderate", col, f"{role} PSI {info['psi']}"))
        if info["missing_cur"] - info["missing_ref"] > args.missing_change:
            flags.append(("major", col, f"missing rate {info['missing_ref']:.1%} -> {info['missing_cur']:.1%}"))
        if info.get("unseen_share", 0) > 0.05:
            flags.append(("moderate", col, f"{info['unseen_share']:.1%} unseen categories, e.g. {info['unseen_examples']}"))
        if info.get("outside_ref_range", 0) > 0.05:
            flags.append(("moderate", col, f"{info['outside_ref_range']:.1%} of values outside the training range"))

    order = {"major": 0, "moderate": 1}
    flags.sort(key=lambda f: (order[f[0]], f[1]))
    schema_changed = bool(schema["missing_in_current"] or schema["new_in_current"] or schema["type_changes"]
                          or schema.get("missing_in_reference"))
    report = {
        "reference_rows": len(ref), "current_rows": len(cur), "schema": schema, "schema_changed": schema_changed,
        "columns": columns, "flags": [{"severity": s, "column": c, "detail": d} for s, c, d in flags],
        "prediction_drift": columns.get(args.prediction_col) if args.prediction_col else None,
    }
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    bands = {b: sum(1 for v in columns.values() if v["band"] == b) for b in ("stable", "moderate", "major")}
    print(f"Drift: {len(ref):,} reference vs {len(cur):,} current rows, {len(columns)} columns "
          f"(stable {bands['stable']}, moderate {bands['moderate']}, major {bands['major']})")
    if schema_changed:
        print(f"  SCHEMA missing: {schema['missing_in_current'] or '-'} | new: {schema['new_in_current'] or '-'} | "
              f"type changes: {schema['type_changes'] or '-'}"
              + (f" | not in reference: {schema['missing_in_reference']}" if schema.get("missing_in_reference") else ""))
    for s, c, d in flags:
        print(f"  {s.upper():8} {c}: {d}")
    if args.prediction_col and args.prediction_col in columns:
        p = columns[args.prediction_col]
        print(f"  prediction '{args.prediction_col}': PSI {p.get('psi')} ({p['band']})")
    print("Drift is a reason to investigate and check labelled performance, not proof of degradation.")
    if args.out:
        print(f"JSON report: {args.out}")
    major = any(s == "major" for s, _, _ in flags)
    return 1 if major or schema_changed else 0


if __name__ == "__main__":
    sys.exit(main())
