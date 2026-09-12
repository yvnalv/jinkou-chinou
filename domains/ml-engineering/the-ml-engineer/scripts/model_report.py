#!/usr/bin/env python3
"""Evaluation report for a model's predictions: metrics with confidence intervals, calibration,
thresholds, baselines, and per-slice performance.

Input: a CSV/Parquet file of predictions on a held-out set, one row per example.

  binary classification   --y-true COL --y-score COL (probability of the positive class) [--positive VALUE]
                          [--threshold 0.5] [--cost-fp 1 --cost-fn 5] -> ROC AUC, PR AUC, log loss, Brier,
                          calibration (ECE + table), metrics at threshold, F1-optimal and cost-optimal thresholds
  multiclass              --y-true COL --y-pred COL [--score-cols a,b,c] -> accuracy, macro/weighted F1,
                          per-class precision/recall, confusion matrix, log loss (with scores)
  regression / forecast   --y-true COL --y-pred COL [--y-baseline COL] -> MAE, RMSE, MedAE, R2, bias,
                          MAPE (non-zero targets), sMAPE, residual quantiles, skill vs a baseline forecast

Common options: --slices seg1,seg2 (metrics per segment), --bootstrap N (95% CIs), --out report.json

Examples:
  python model_report.py preds.csv --task binary --y-true churned --y-score p_churn --cost-fp 1 --cost-fn 8 --slices plan,region
  python model_report.py preds.csv --task regression --y-true sales --y-pred forecast --y-baseline seasonal_naive
  python model_report.py preds.csv --task multiclass --y-true label --y-pred pred --score-cols p_cat,p_dog,p_bird

Requires pandas and numpy (no scikit-learn needed).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.exit("model_report.py needs pandas and numpy: pip install pandas numpy")

EPS = 1e-15


def read_any(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.is_file():
        sys.exit(f"error: file not found: {path}")
    if p.suffix.lower() in (".parquet", ".pq"):
        return pd.read_parquet(p)
    if p.suffix.lower() in (".jsonl", ".ndjson"):
        return pd.read_json(p, lines=True)
    return pd.read_csv(p, low_memory=False)


def r(x, digits: int = 4):
    if x is None:
        return None
    x = float(x)
    return None if math.isnan(x) or math.isinf(x) else round(x, digits)


# ---------------------------------------------------------------------------
# Binary classification
# ---------------------------------------------------------------------------

def roc_auc(y: np.ndarray, s: np.ndarray) -> float | None:
    pos = y == 1
    n_pos, n_neg = int(pos.sum()), int((~pos).sum())
    if not n_pos or not n_neg:
        return None
    ranks = pd.Series(s).rank(method="average").to_numpy()
    return (ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def average_precision(y: np.ndarray, s: np.ndarray) -> float | None:
    """AP = sum over distinct thresholds of (recall step) x precision; tied scores form one threshold."""
    if y.sum() == 0:
        return None
    order = np.argsort(-s, kind="mergesort")
    s_sorted, y_sorted = s[order], y[order]
    last_of_tie = np.r_[np.where(np.diff(s_sorted))[0], len(s_sorted) - 1]
    tp = np.cumsum(y_sorted)[last_of_tie]
    precision = tp / (last_of_tie + 1)
    recall = tp / y.sum()
    return float(np.sum(np.diff(np.r_[0.0, recall]) * precision))


def binary_at(y: np.ndarray, s: np.ndarray, t: float) -> dict:
    pred = s >= t
    tp = int((pred & (y == 1)).sum())
    fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum())
    tn = int((~pred & (y == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "threshold": r(t), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "accuracy": r((tp + tn) / len(y)), "precision": r(precision), "recall": r(recall),
        "specificity": r(tn / (tn + fp) if tn + fp else 0.0),
        "f1": r(2 * precision * recall / (precision + recall) if precision + recall else 0.0),
        "predicted_positive_rate": r(pred.mean()),
    }


def calibration(y: np.ndarray, s: np.ndarray, bins: int = 10) -> tuple[float, list[dict]]:
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.digitize(s, edges[1:-1]), 0, bins - 1)
    table, ece = [], 0.0
    for b in range(bins):
        m = idx == b
        if not m.any():
            continue
        conf, acc = float(s[m].mean()), float(y[m].mean())
        ece += m.mean() * abs(conf - acc)
        table.append({"bin": f"{edges[b]:.1f}-{edges[b + 1]:.1f}", "n": int(m.sum()),
                      "mean_predicted": r(conf), "observed_rate": r(acc)})
    return float(ece), table


def binary_metrics(y: np.ndarray, s: np.ndarray, threshold: float) -> dict:
    s_clip = np.clip(s, EPS, 1 - EPS)
    prevalence = float(y.mean())
    brier = float(np.mean((s - y) ** 2))
    brier_ref = prevalence * (1 - prevalence)
    ece, _ = calibration(y, s)
    return {
        "n": int(len(y)), "prevalence": r(prevalence),
        "roc_auc": r(roc_auc(y, s)), "pr_auc": r(average_precision(y, s)), "pr_auc_baseline": r(prevalence),
        "log_loss": r(-np.mean(y * np.log(s_clip) + (1 - y) * np.log(1 - s_clip))),
        "brier": r(brier), "brier_skill_vs_prevalence": r(1 - brier / brier_ref) if brier_ref else None,
        "ece": r(ece), "at_threshold": binary_at(y, s, threshold),
    }


def best_thresholds(y: np.ndarray, s: np.ndarray, cost_fp: float | None, cost_fn: float | None) -> dict:
    candidates = np.unique(np.quantile(s, np.linspace(0.005, 0.995, 199)))
    best_f1 = max((binary_at(y, s, t) for t in candidates), key=lambda m: m["f1"])
    out = {"f1_optimal": best_f1}
    if cost_fp is not None and cost_fn is not None:
        def cost(m):
            return m["fp"] * cost_fp + m["fn"] * cost_fn
        best = min((binary_at(y, s, t) for t in candidates), key=cost)
        best["total_cost"] = r(cost(best))
        best["cost_per_example"] = r(cost(best) / len(y))
        out["cost_optimal"] = best
        out["cost_note"] = f"costs: false positive {cost_fp}, false negative {cost_fn}; choose thresholds on validation data, not test"
    return out


# ---------------------------------------------------------------------------
# Multiclass and regression
# ---------------------------------------------------------------------------

def multiclass_metrics(y_true: pd.Series, y_pred: pd.Series, scores: pd.DataFrame | None) -> dict:
    labels = sorted(set(y_true.astype(str)) | set(y_pred.astype(str)))
    yt, yp = y_true.astype(str).to_numpy(), y_pred.astype(str).to_numpy()
    per_class, f1s, supports = {}, [], []
    for c in labels:
        tp = int(((yp == c) & (yt == c)).sum())
        fp = int(((yp == c) & (yt != c)).sum())
        fn = int(((yp != c) & (yt == c)).sum())
        p = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * p * rc / (p + rc) if p + rc else 0.0
        support = int((yt == c).sum())
        per_class[c] = {"precision": r(p), "recall": r(rc), "f1": r(f1), "support": support}
        f1s.append(f1)
        supports.append(support)
    confusion = pd.crosstab(pd.Series(yt, name="true"), pd.Series(yp, name="pred")).reindex(index=labels, columns=labels, fill_value=0)
    out = {
        "n": int(len(yt)), "accuracy": r((yt == yp).mean()),
        "macro_f1": r(np.mean(f1s)), "weighted_f1": r(np.average(f1s, weights=supports) if sum(supports) else 0),
        "majority_class_accuracy": r(pd.Series(yt).value_counts(normalize=True).iloc[0]),
        "per_class": per_class, "confusion_matrix": {"labels": labels, "rows_true_cols_pred": confusion.to_numpy().tolist()},
    }
    if scores is not None:
        col_for = {c.split("_", 1)[-1] if c.startswith("p_") else c: c for c in scores.columns}
        missing = [c for c in labels if c not in col_for]
        if not missing:
            probs = scores[[col_for[c] for c in labels]].to_numpy(dtype=float)
            probs = probs / probs.sum(axis=1, keepdims=True)
            true_idx = np.array([labels.index(v) for v in yt])
            out["log_loss"] = r(-np.mean(np.log(np.clip(probs[np.arange(len(yt)), true_idx], EPS, 1))))
        else:
            out["log_loss_note"] = f"score columns do not cover labels {missing} (name them p_<label> or <label>)"
    return out


def regression_metrics(y: np.ndarray, p: np.ndarray, baseline: np.ndarray | None) -> dict:
    err = p - y
    abs_err = np.abs(err)
    nonzero = y != 0
    ss_res, ss_tot = float(np.sum(err ** 2)), float(np.sum((y - y.mean()) ** 2))
    out = {
        "n": int(len(y)), "mae": r(abs_err.mean()), "rmse": r(math.sqrt(np.mean(err ** 2))),
        "median_ae": r(np.median(abs_err)), "r2": r(1 - ss_res / ss_tot) if ss_tot else None,
        "bias_mean_error": r(err.mean()),
        "mape": r(np.mean(abs_err[nonzero] / np.abs(y[nonzero]))) if nonzero.any() else None,
        "mape_note": f"{int((~nonzero).sum())} zero targets excluded from MAPE" if (~nonzero).any() else None,
        "smape": r(np.mean(2 * abs_err / np.clip(np.abs(y) + np.abs(p), EPS, None))),
        "residual_quantiles": {q: r(np.quantile(err, float(q))) for q in ("0.05", "0.25", "0.5", "0.75", "0.95")},
        "mean_predictor_mae": r(np.mean(np.abs(y - y.mean()))),
    }
    if baseline is not None:
        base_mae = float(np.mean(np.abs(baseline - y)))
        out["baseline_mae"] = r(base_mae)
        out["mae_skill_vs_baseline"] = r(1 - out["mae"] / base_mae) if base_mae else None
        out["relative_mae"] = r(out["mae"] / base_mae) if base_mae else None
    return out


# ---------------------------------------------------------------------------
# Bootstrap and slices
# ---------------------------------------------------------------------------

def bootstrap_ci(fn, n: int, reps: int, seed: int = 0) -> tuple[float | None, float | None]:
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        v = fn(idx)
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            values.append(v)
    if len(values) < reps * 0.5:
        return None, None
    return r(np.quantile(values, 0.025)), r(np.quantile(values, 0.975))


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="See the module docstring for inputs per task.")
    parser.add_argument("predictions", help="CSV / Parquet / JSONL with true values and predictions")
    parser.add_argument("--task", choices=("binary", "multiclass", "regression"), required=True)
    parser.add_argument("--y-true", required=True)
    parser.add_argument("--y-score", help="binary: probability of the positive class")
    parser.add_argument("--y-pred", help="multiclass label or regression prediction")
    parser.add_argument("--y-baseline", help="regression: baseline prediction column (e.g. seasonal naive)")
    parser.add_argument("--score-cols", help="multiclass: comma list of probability columns")
    parser.add_argument("--positive", help="binary: value of y-true that is the positive class (default: 1/True)")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--cost-fp", type=float)
    parser.add_argument("--cost-fn", type=float)
    parser.add_argument("--slices", default="", help="comma list of segment columns")
    parser.add_argument("--min-slice", type=int, default=30, help="skip slices smaller than this")
    parser.add_argument("--bootstrap", type=int, default=500, help="bootstrap repetitions for CIs (0 to skip)")
    parser.add_argument("--out", help="write JSON report")
    args = parser.parse_args(argv)

    df = read_any(args.predictions)
    need = [args.y_true] + [c for c in (args.y_score, args.y_pred, args.y_baseline) if c] + \
           [c for c in args.slices.split(",") if c] + [c for c in (args.score_cols or "").split(",") if c]
    missing = [c for c in need if c not in df.columns]
    if missing:
        sys.exit(f"error: missing columns: {missing}. Available: {list(df.columns)}")
    before = len(df)
    df = df.dropna(subset=[c for c in (args.y_true, args.y_score, args.y_pred) if c])
    report: dict = {"task": args.task, "rows": len(df), "rows_dropped_missing": before - len(df)}
    slices = [c for c in args.slices.split(",") if c]

    if args.task == "binary":
        if not args.y_score:
            sys.exit("error: binary needs --y-score (probabilities); hard labels hide ranking and calibration")
        raw = df[args.y_true]
        if args.positive is not None:
            y = (raw.astype(str) == args.positive).astype(int).to_numpy()
        else:
            y = raw.map(lambda v: 1 if v in (1, True, "1", "true", "True", "yes") else 0).to_numpy()
        s = df[args.y_score].astype(float).to_numpy()
        if s.min() < 0 or s.max() > 1:
            sys.exit("error: --y-score must be probabilities in [0, 1]")
        report["overall"] = binary_metrics(y, s, args.threshold)
        report["thresholds"] = best_thresholds(y, s, args.cost_fp, args.cost_fn)
        _, report["calibration_table"] = calibration(y, s)
        if args.bootstrap:
            report["ci95"] = {
                "roc_auc": bootstrap_ci(lambda i: roc_auc(y[i], s[i]), len(y), args.bootstrap),
                "pr_auc": bootstrap_ci(lambda i: average_precision(y[i], s[i]), len(y), args.bootstrap),
                "recall_at_threshold": bootstrap_ci(lambda i: binary_at(y[i], s[i], args.threshold)["recall"], len(y), args.bootstrap),
                "precision_at_threshold": bootstrap_ci(lambda i: binary_at(y[i], s[i], args.threshold)["precision"], len(y), args.bootstrap),
            }
        slice_fn = lambda m: {k: v for k, v in binary_metrics(y[m], s[m], args.threshold).items() if k != "at_threshold"} | {
            "recall": binary_metrics(y[m], s[m], args.threshold)["at_threshold"]["recall"],
            "precision": binary_metrics(y[m], s[m], args.threshold)["at_threshold"]["precision"]}
        key_metric = "roc_auc"
    elif args.task == "multiclass":
        if not args.y_pred:
            sys.exit("error: multiclass needs --y-pred")
        scores = df[args.score_cols.split(",")] if args.score_cols else None
        report["overall"] = multiclass_metrics(df[args.y_true], df[args.y_pred], scores)
        yt, yp = df[args.y_true].astype(str).to_numpy(), df[args.y_pred].astype(str).to_numpy()
        if args.bootstrap:
            report["ci95"] = {"accuracy": bootstrap_ci(lambda i: float((yt[i] == yp[i]).mean()), len(yt), args.bootstrap)}
        slice_fn = lambda m: {k: v for k, v in multiclass_metrics(df[args.y_true][m], df[args.y_pred][m], None).items()
                              if k in ("n", "accuracy", "macro_f1")}
        key_metric = "macro_f1"
    else:
        if not args.y_pred:
            sys.exit("error: regression needs --y-pred")
        y = df[args.y_true].astype(float).to_numpy()
        p = df[args.y_pred].astype(float).to_numpy()
        b = df[args.y_baseline].astype(float).to_numpy() if args.y_baseline else None
        report["overall"] = regression_metrics(y, p, b)
        if args.bootstrap:
            report["ci95"] = {
                "mae": bootstrap_ci(lambda i: float(np.mean(np.abs(p[i] - y[i]))), len(y), args.bootstrap),
                "rmse": bootstrap_ci(lambda i: float(math.sqrt(np.mean((p[i] - y[i]) ** 2))), len(y), args.bootstrap),
            }
            if b is not None:
                report["ci95"]["mae_difference_vs_baseline"] = bootstrap_ci(
                    lambda i: float(np.mean(np.abs(p[i] - y[i])) - np.mean(np.abs(b[i] - y[i]))), len(y), args.bootstrap)
        slice_fn = lambda m: {k: v for k, v in regression_metrics(y[m], p[m], b[m] if b is not None else None).items()
                              if k in ("n", "mae", "rmse", "bias_mean_error", "r2")}
        key_metric = "mae"

    # Slices
    report["slices"] = {}
    warnings = []
    overall_key = report["overall"].get(key_metric)
    for col in slices:
        report["slices"][col] = {}
        for value, idx in df.groupby(col, dropna=False).indices.items():
            if len(idx) < args.min_slice:
                continue
            mask = np.zeros(len(df), dtype=bool)
            mask[idx] = True
            metrics = slice_fn(mask)
            report["slices"][col][str(value)] = metrics
            v = metrics.get(key_metric)
            if v is not None and overall_key is not None:
                worse = (v > overall_key * 1.2) if key_metric == "mae" else (v < overall_key - 0.05)
                if worse:
                    warnings.append(f"slice {col}={value} (n={len(idx)}): {key_metric} {v} vs overall {overall_key}")
    report["slice_warnings"] = warnings

    # Printed summary
    o = report["overall"]
    print(f"{args.task} evaluation on {report['rows']:,} rows ({report['rows_dropped_missing']} dropped for missing values)")
    ci = report.get("ci95", {})
    if args.task == "binary":
        print(f"  prevalence {o['prevalence']} | ROC AUC {o['roc_auc']} {ci.get('roc_auc', '')} | "
              f"PR AUC {o['pr_auc']} (baseline {o['pr_auc_baseline']}) {ci.get('pr_auc', '')}")
        print(f"  log loss {o['log_loss']} | Brier {o['brier']} (skill vs prevalence {o['brier_skill_vs_prevalence']}) | ECE {o['ece']}")
        a = o["at_threshold"]
        print(f"  at threshold {a['threshold']}: precision {a['precision']} recall {a['recall']} F1 {a['f1']} "
              f"(TP {a['tp']} FP {a['fp']} FN {a['fn']} TN {a['tn']})")
        t = report["thresholds"]
        print(f"  F1-optimal threshold {t['f1_optimal']['threshold']} (F1 {t['f1_optimal']['f1']})")
        if "cost_optimal" in t:
            c = t["cost_optimal"]
            print(f"  cost-optimal threshold {c['threshold']} (cost/example {c['cost_per_example']}, recall {c['recall']}, precision {c['precision']})")
        if o["ece"] and o["ece"] > 0.05:
            print("  note: ECE above 0.05; calibrate (isotonic or Platt on validation data) before using scores as probabilities")
    elif args.task == "multiclass":
        print(f"  accuracy {o['accuracy']} {ci.get('accuracy', '')} (majority-class baseline {o['majority_class_accuracy']}) | "
              f"macro F1 {o['macro_f1']} | weighted F1 {o['weighted_f1']}" + (f" | log loss {o['log_loss']}" if "log_loss" in o else ""))
        worst = sorted(o["per_class"].items(), key=lambda kv: kv[1]["f1"])[:3]
        print("  weakest classes: " + ", ".join(f"{c} (F1 {m['f1']}, n={m['support']})" for c, m in worst))
    else:
        print(f"  MAE {o['mae']} {ci.get('mae', '')} | RMSE {o['rmse']} | MedAE {o['median_ae']} | R2 {o['r2']} | bias {o['bias_mean_error']}")
        print(f"  MAPE {o['mape']} | sMAPE {o['smape']} | mean-predictor MAE {o['mean_predictor_mae']}")
        if "baseline_mae" in o:
            print(f"  vs baseline: MAE {o['baseline_mae']} -> skill {o['mae_skill_vs_baseline']} "
                  f"(difference CI {ci.get('mae_difference_vs_baseline')})")
    for w in warnings:
        print(f"  SLICE WARNING {w}")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        print(f"JSON report: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
