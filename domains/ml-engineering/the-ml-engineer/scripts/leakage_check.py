#!/usr/bin/env python3
"""Detect data leakage and split problems before trusting a model's validation score.

Checks a train/test split (two files, or one file with a split column):
  * exact duplicate rows shared by train and test (ignoring the target)
  * entity overlap: the same ID or group value in both splits (use --id / --group)
  * temporal overlap: test rows dated before the end of training data (use --time)
  * single-feature leakage suspects: one feature alone almost perfectly predicts the target
    (out-of-fold univariate AUC for classification, |Spearman| for regression)
  * suspicious feature names (words that often mean "known after the outcome")
  * ID-like features (unique per row) used as model inputs
  * train/test distribution shift per feature (PSI) and target balance difference
  * adversarial validation (optional, needs scikit-learn): can a model tell train from test?

Examples:
  python leakage_check.py --train train.csv --test test.csv --target churned --id customer_id --time signup_date
  python leakage_check.py --data all.parquet --split-col split --target price --task regression --out leakage.json

Exit code 1 when high-severity findings exist (useful as a CI gate).
Requires pandas and numpy; scikit-learn is optional (adversarial validation).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.exit("leakage_check.py needs pandas and numpy: pip install pandas numpy")

SUSPICIOUS_TOKENS = {
    "label", "target", "outcome", "result", "future", "after", "post", "next", "final", "resolution",
    "resolved", "closed", "cancel", "cancelled", "canceled", "churned", "default", "defaulted", "outcome",
    "approved", "refund", "chargeback", "returned", "converted", "won", "lost", "status", "flag",
}
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def read_any(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.is_file():
        sys.exit(f"error: file not found: {path}")
    ext = p.suffix.lower()
    if ext in (".parquet", ".pq"):
        return pd.read_parquet(p)
    if ext in (".jsonl", ".ndjson"):
        return pd.read_json(p, lines=True)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(p)
    return pd.read_csv(p, low_memory=False)


def tokens(name: str) -> set[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    return {t for t in re.split(r"[^a-z0-9]+", spaced.lower()) if t}


def rank_auc(score: np.ndarray, y: np.ndarray) -> float | None:
    """ROC AUC via the Mann-Whitney U statistic (ties get average ranks)."""
    mask = ~np.isnan(score)
    score, y = score[mask], y[mask]
    pos = y == 1
    n_pos, n_neg = int(pos.sum()), int((~pos).sum())
    if n_pos == 0 or n_neg == 0:
        return None
    ranks = pd.Series(score).rank(method="average").to_numpy()
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def oof_target_encode(x: pd.Series, y: np.ndarray, folds: int = 5, seed: int = 0) -> np.ndarray:
    """Out-of-fold mean-target encoding, so high-cardinality columns do not look predictive by memorization."""
    rng = np.random.default_rng(seed)
    fold_ids = rng.integers(0, folds, size=len(x))
    out = np.full(len(x), np.nan)
    keys = x.astype("object").where(x.notna(), "__missing__").to_numpy()
    prior = float(np.mean(y))
    for f in range(folds):
        train_mask = fold_ids != f
        means = pd.Series(y[train_mask]).groupby(keys[train_mask]).mean()
        out[~train_mask] = pd.Series(keys[~train_mask]).map(means).fillna(prior).to_numpy()
    return out


def psi(ref: pd.Series, cur: pd.Series, bins: int = 10) -> float | None:
    ref, cur = ref.dropna(), cur.dropna()
    if ref.empty or cur.empty:
        return None
    if pd.api.types.is_numeric_dtype(ref) and ref.nunique() > bins:
        edges = np.unique(np.quantile(ref.astype(float), np.linspace(0, 1, bins + 1)))
        if len(edges) < 3:
            return None
        edges[0], edges[-1] = -np.inf, np.inf
        r = np.histogram(ref.astype(float), edges)[0] / len(ref)
        c = np.histogram(cur.astype(float), edges)[0] / len(cur)
    else:
        top = ref.astype(str).value_counts().index[:30]
        r_counts = ref.astype(str).where(ref.astype(str).isin(top), "__other__").value_counts(normalize=True)
        c_counts = cur.astype(str).where(cur.astype(str).isin(top), "__other__").value_counts(normalize=True)
        cats = r_counts.index.union(c_counts.index)
        r = r_counts.reindex(cats, fill_value=0).to_numpy()
        c = c_counts.reindex(cats, fill_value=0).to_numpy()
    r = np.clip(r, 1e-4, None)
    c = np.clip(c, 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))


def to_binary(y: pd.Series) -> np.ndarray:
    """Binary targets as 0/1; multiclass collapsed to 'majority class vs rest' for screening."""
    values = y.dropna().unique()
    if len(values) == 2:
        positive = sorted(values, key=lambda v: (y == v).sum())[0]  # minority class as positive
        return (y == positive).astype(int).to_numpy()
    majority = y.value_counts().index[0]
    return (y != majority).astype(int).to_numpy()


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for the full list of checks.")
    parser.add_argument("--train", help="training file (csv, parquet, jsonl, xlsx)")
    parser.add_argument("--test", help="test / validation file")
    parser.add_argument("--data", help="single file containing both splits (with --split-col)")
    parser.add_argument("--split-col", help="column whose values mark train and test rows")
    parser.add_argument("--train-value", default="train")
    parser.add_argument("--test-value", default="test")
    parser.add_argument("--target", required=True)
    parser.add_argument("--task", choices=("classification", "regression", "auto"), default="auto")
    parser.add_argument("--id", help="entity ID column (customer, patient, device …); must not span splits")
    parser.add_argument("--group", help="grouping column that must not span splits (e.g. store, user)")
    parser.add_argument("--time", help="event-time column; test should come after train for temporal problems")
    parser.add_argument("--exclude", default="", help="comma list of columns that are not model features")
    parser.add_argument("--auc-threshold", type=float, default=0.95, help="single-feature separability flagged as leakage")
    parser.add_argument("--no-adversarial", action="store_true", help="skip adversarial validation")
    parser.add_argument("--out", help="write the JSON report here")
    args = parser.parse_args(argv)

    if args.data:
        if not args.split_col:
            sys.exit("error: --data needs --split-col")
        df = read_any(args.data)
        train = df[df[args.split_col].astype(str) == args.train_value].drop(columns=[args.split_col])
        test = df[df[args.split_col].astype(str) == args.test_value].drop(columns=[args.split_col])
    elif args.train and args.test:
        train, test = read_any(args.train), read_any(args.test)
    else:
        sys.exit("error: give --train and --test, or --data with --split-col")
    if train.empty or test.empty:
        sys.exit("error: train or test split is empty")
    for col in [args.target] + [c for c in (args.id, args.group, args.time) if c]:
        if col not in train.columns or col not in test.columns:
            sys.exit(f"error: column '{col}' missing from train or test")

    findings: list[dict] = []

    def add(severity: str, check: str, detail: str, column: str | None = None, value=None) -> None:
        findings.append({"severity": severity, "check": check, "column": column, "detail": detail, "value": value})

    task = args.task
    if task == "auto":
        y_all = pd.concat([train[args.target], test[args.target]])
        task = "classification" if (not pd.api.types.is_numeric_dtype(y_all) or y_all.nunique() <= 20) else "regression"

    non_features = {args.target} | {c for c in (args.id, args.group, args.time) if c} | {c for c in args.exclude.split(",") if c}
    features = [c for c in train.columns if c not in non_features and c in test.columns]

    # 1. Exact duplicates across splits (ignoring target)
    compare_cols = [c for c in train.columns if c != args.target and c in test.columns]
    train_keys = set(pd.util.hash_pandas_object(train[compare_cols], index=False).to_numpy())
    test_hash = pd.util.hash_pandas_object(test[compare_cols], index=False).to_numpy()
    dup = int(np.isin(test_hash, list(train_keys)).sum())
    if dup:
        pct = dup / len(test)
        add("high" if pct > 0.01 else "medium", "duplicate_rows_across_splits",
            f"{dup} test rows ({pct:.1%}) also appear in train", value=dup)

    # 2. Entity / group overlap
    for col in (args.id, args.group):
        if col:
            shared = set(train[col].dropna().unique()) & set(test[col].dropna().unique())
            if shared:
                rows = int(test[col].isin(shared).sum())
                add("high", "entity_overlap", f"{len(shared)} {col} values occur in both splits ({rows} test rows, "
                    f"{rows / len(test):.1%}); split by {col} (GroupKFold) so the model is tested on unseen entities",
                    column=col, value=len(shared))

    # 3. Temporal overlap
    if args.time:
        t_train = pd.to_datetime(train[args.time], errors="coerce")
        t_test = pd.to_datetime(test[args.time], errors="coerce")
        if t_train.notna().any() and t_test.notna().any():
            train_max = t_train.max()
            early = int((t_test < train_max).sum())
            if early:
                add("high" if early / len(test) > 0.05 else "medium", "temporal_overlap",
                    f"{early} test rows ({early / len(test):.1%}) are dated before the last training row ({train_max.date()}); "
                    "for forecasting or future-facing predictions use an out-of-time split", column=args.time, value=early)

    # 4. Target sanity
    for name, part in (("train", train), ("test", test)):
        missing = int(part[args.target].isna().sum())
        if missing:
            add("medium", "missing_target", f"{missing} {name} rows have no target", column=args.target, value=missing)
    if task == "classification":
        tr = train[args.target].value_counts(normalize=True)
        te = test[args.target].value_counts(normalize=True)
        gap = float((tr.reindex(tr.index.union(te.index), fill_value=0) - te.reindex(tr.index.union(te.index), fill_value=0)).abs().max())
        if gap > 0.05:
            add("medium", "target_balance_shift", f"class shares differ by up to {gap:.1%} between train and test", value=round(gap, 4))
    else:
        tm, sm = float(train[args.target].mean()), float(test[args.target].mean())
        sd = float(train[args.target].std() or 1)
        if abs(tm - sm) / sd > 0.25:
            add("medium", "target_mean_shift", f"target mean {tm:.4g} (train) vs {sm:.4g} (test)", value=round((sm - tm) / sd, 3))

    # 5. Single-feature leakage suspects (on train)
    y_train = train[args.target]
    keep = y_train.notna().to_numpy()
    strengths = {}
    if task == "classification":
        yb = to_binary(y_train[keep])
    for col in features:
        x = train.loc[keep, col]
        if x.nunique(dropna=True) <= 1:
            continue
        try:
            if task == "classification":
                if pd.api.types.is_numeric_dtype(x) and x.nunique() > 20:
                    auc = rank_auc(x.astype(float).to_numpy(), yb)
                else:
                    auc = rank_auc(oof_target_encode(x, yb), yb)
                if auc is None:
                    continue
                strength = max(auc, 1 - auc)
            else:
                yr = y_train[keep].astype(float)
                score = x.astype(float) if pd.api.types.is_numeric_dtype(x) else pd.Series(oof_target_encode(x, yr.to_numpy()), index=x.index)
                strength = abs(float(pd.Series(score).corr(yr, method="spearman")))
        except (TypeError, ValueError):
            continue
        if np.isnan(strength):
            continue
        strengths[col] = round(float(strength), 4)
        if strength >= args.auc_threshold:
            add("high", "single_feature_leakage_suspect",
                f"'{col}' alone gives separability {strength:.3f}; check it is known at prediction time and not derived from the target",
                column=col, value=round(float(strength), 4))

    # 6. Suspicious names and ID-like features
    target_tokens = tokens(args.target)
    for col in features:
        hits = (tokens(col) & SUSPICIOUS_TOKENS) | (tokens(col) & target_tokens)
        if hits:
            add("low", "suspicious_name", f"'{col}' contains {sorted(hits)}; confirm it is available before the outcome", column=col)
        x = train[col]
        if len(x) > 50 and x.nunique(dropna=True) / max(1, x.notna().sum()) > 0.98 and not (
                pd.api.types.is_float_dtype(x) and x.round().ne(x).any()):
            add("medium", "id_like_feature", f"'{col}' is unique per row (an identifier?); IDs memorize rows and leak ordering",
                column=col)

    # 7. Distribution shift between splits
    shifts = {}
    for col in features:
        value = psi(train[col], test[col])
        if value is not None:
            shifts[col] = round(value, 4)
            if value > 0.25:
                add("medium", "split_distribution_shift", f"'{col}' PSI {value:.2f} between train and test "
                    "(expected for out-of-time splits; unexpected for random splits)", column=col, value=round(value, 4))

    # 8. Adversarial validation
    adversarial = None
    if not args.no_adversarial:
        try:
            from sklearn.ensemble import HistGradientBoostingClassifier
            from sklearn.model_selection import cross_val_predict
        except ImportError:
            adversarial = {"skipped": "scikit-learn not installed"}
        else:
            both = pd.concat([train[features], test[features]], ignore_index=True)
            enc = pd.DataFrame(index=both.index)
            for col in features:
                enc[col] = both[col] if pd.api.types.is_numeric_dtype(both[col]) else both[col].astype("category").cat.codes
            is_test = np.r_[np.zeros(len(train)), np.ones(len(test))]
            n = min(len(enc), 20000)
            idx = np.random.default_rng(0).choice(len(enc), size=n, replace=False)
            proba = cross_val_predict(HistGradientBoostingClassifier(max_iter=100, random_state=0),
                                      enc.iloc[idx], is_test[idx], cv=3, method="predict_proba")[:, 1]
            adv_auc = rank_auc(proba, is_test[idx].astype(int))
            adversarial = {"auc": round(adv_auc, 4) if adv_auc is not None else None}
            if adv_auc and adv_auc > 0.8:
                top = sorted(shifts.items(), key=lambda kv: -kv[1])[:5]
                add("medium", "adversarial_validation",
                    f"a model separates train from test with AUC {adv_auc:.2f}; the splits differ systematically "
                    f"(most shifted: {', '.join(c for c, _ in top)})", value=round(adv_auc, 4))

    findings.sort(key=lambda f: SEVERITY_ORDER[f["severity"]])
    report = {
        "task": task, "train_rows": len(train), "test_rows": len(test), "features_checked": len(features),
        "findings": findings,
        "single_feature_strength_top": dict(sorted(strengths.items(), key=lambda kv: -kv[1])[:15]),
        "psi_top": dict(sorted(shifts.items(), key=lambda kv: -kv[1])[:15]),
        "adversarial_validation": adversarial,
        "not_checked": ["whether each feature is known at prediction time (needs domain knowledge)",
                        "preprocessing fitted on all data before splitting (check the pipeline code)",
                        "feature selection or tuning done on the test set (check the workflow)"],
    }
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
    print(f"Leakage check ({task}): {len(train):,} train / {len(test):,} test rows, {len(features)} features")
    print(f"Findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low")
    for f in findings:
        print(f"  {f['severity'].upper():6} {f['check']}: {f['detail']}")
    if adversarial and "auc" in adversarial:
        print(f"Adversarial validation AUC: {adversarial['auc']} (about 0.5 means train and test look alike)")
    print("Not checkable automatically: " + "; ".join(report["not_checked"]) + ".")
    if args.out:
        print(f"JSON report: {args.out}")
    return 1 if counts["high"] else 0


if __name__ == "__main__":
    sys.exit(main())
