"""Training pipeline template for tabular models (scikit-learn, optional MLflow). Copy into the project
as e.g. src/train.py and adapt engineer_features() and the candidate models.

What it does, in order:
  1. loads data and drops rows without a target
  2. locks a test set using the right split for the problem: random/stratified, group (unseen
     entities), or time (out-of-time)
  3. cross-validates baselines and candidates on the training part only, with the matching CV scheme
  4. picks the best candidate by mean CV score, refits it on all training data
  5. evaluates it ONCE on the locked test set and writes test predictions (for model_report.py)
  6. saves the model, metadata (features, dtypes, metrics, versions, data hash), and logs to MLflow
     if installed and --mlflow is given

Example:
  python train_pipeline.py --data data/churn.csv --target churned --task classification \
      --split time --time-col event_date --group-col customer_id --drop customer_id --out models/churn
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

SEED = 42


# ---------------------------------------------------------------------------
# 1. Features: adapt this to the problem. Use only information available at prediction time.
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame, time_col: str | None) -> pd.DataFrame:
    df = df.copy()
    if time_col and time_col in df.columns:
        t = pd.to_datetime(df[time_col], errors="coerce")
        df["event_dayofweek"] = t.dt.dayofweek
        df["event_month"] = t.dt.month
    return df


# ---------------------------------------------------------------------------
# 2. Splits
# ---------------------------------------------------------------------------

def split_test(df: pd.DataFrame, args) -> tuple[pd.DataFrame, pd.DataFrame]:
    if args.split == "time":
        order = pd.to_datetime(df[args.time_col], errors="coerce").sort_values(kind="mergesort").index
        cut = int(len(order) * (1 - args.test_size))
        train, test = df.loc[order[:cut]], df.loc[order[cut:]]
        if args.group_col:  # also keep test entities unseen, if an entity column is given
            before = len(test)
            test = test[~test[args.group_col].isin(set(train[args.group_col]))]
            if len(test) < 0.5 * before:
                print(f"note: {before - len(test)} of {before} out-of-time test rows belong to entities seen in training "
                      "and were removed; drop --group-col if repeat entities are expected in production", file=sys.stderr)
        return train, test
    if args.split == "group":
        gss = GroupShuffleSplit(n_splits=1, test_size=args.test_size, random_state=SEED)
        tr, te = next(gss.split(df, groups=df[args.group_col]))
        return df.iloc[tr], df.iloc[te]
    stratify = df[args.target] if args.task == "classification" else None
    return train_test_split(df, test_size=args.test_size, random_state=SEED, stratify=stratify)


def cv_scheme(args, train: pd.DataFrame):
    if args.split == "time":
        return TimeSeriesSplit(n_splits=args.folds), None
    if args.split == "group":
        return GroupKFold(n_splits=args.folds), train[args.group_col]
    if args.task == "classification":
        return StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=SEED), None
    return KFold(n_splits=args.folds, shuffle=True, random_state=SEED), None


# ---------------------------------------------------------------------------
# 3. Models: baselines first, then candidates
# ---------------------------------------------------------------------------

def build_models(task: str, numeric: list[str], categorical: list[str]) -> dict[str, Pipeline]:
    linear_prep = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median", add_indicator=True)), ("scale", StandardScaler())]), numeric),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=20))]), categorical),
    ])
    tree_prep = ColumnTransformer([
        ("num", "passthrough", numeric),  # HistGradientBoosting handles missing values natively
        ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-2), categorical),
    ])
    cat_mask = [False] * len(numeric) + [True] * len(categorical)
    if task == "classification":
        return {
            "baseline_prior": Pipeline([("prep", linear_prep), ("model", DummyClassifier(strategy="prior"))]),
            "logistic_regression": Pipeline([("prep", linear_prep), ("model", LogisticRegression(max_iter=2000, C=1.0))]),
            "hist_gradient_boosting": Pipeline([("prep", tree_prep), ("model", HistGradientBoostingClassifier(
                categorical_features=cat_mask, learning_rate=0.05, max_iter=400, early_stopping=True, random_state=SEED))]),
        }
    return {
        "baseline_mean": Pipeline([("prep", linear_prep), ("model", DummyRegressor(strategy="mean"))]),
        "ridge": Pipeline([("prep", linear_prep), ("model", Ridge(alpha=1.0))]),
        "hist_gradient_boosting": Pipeline([("prep", tree_prep), ("model", HistGradientBoostingRegressor(
            categorical_features=cat_mask, learning_rate=0.05, max_iter=400, early_stopping=True, random_state=SEED))]),
    }


# ---------------------------------------------------------------------------
# 4. Run
# ---------------------------------------------------------------------------

def git_commit() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train and evaluate a tabular model with a locked test set.")
    parser.add_argument("--data", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--task", choices=("classification", "regression"), required=True)
    parser.add_argument("--split", choices=("random", "group", "time"), default="random")
    parser.add_argument("--time-col")
    parser.add_argument("--group-col")
    parser.add_argument("--drop", default="", help="comma list of non-feature columns (IDs, raw timestamps, leaks)")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--metric", help="scikit-learn scorer (default: roc_auc / neg_mean_absolute_error)")
    parser.add_argument("--out", default="models/latest")
    parser.add_argument("--mlflow", action="store_true", help="log to MLflow (needs mlflow installed)")
    parser.add_argument("--experiment", default="default")
    args = parser.parse_args(argv)
    if args.split == "time" and not args.time_col:
        parser.error("--split time needs --time-col")
    if args.split == "group" and not args.group_col:
        parser.error("--split group needs --group-col")

    raw_bytes = Path(args.data).read_bytes()
    df = pd.read_csv(args.data) if args.data.endswith(".csv") else pd.read_parquet(args.data)
    df = df.dropna(subset=[args.target]).reset_index(drop=True)
    df = engineer_features(df, args.time_col)
    if args.task == "classification" and df[args.target].nunique() != 2:
        scorer_default = "f1_macro"
    else:
        scorer_default = "roc_auc" if args.task == "classification" else "neg_mean_absolute_error"
    metric = args.metric or scorer_default

    train, test = split_test(df, args)
    drop = {c for c in args.drop.split(",") if c} | {args.target} | ({args.time_col} if args.time_col else set())
    features = [c for c in df.columns if c not in drop]
    numeric = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
    categorical = [c for c in features if c not in numeric]
    X_train, y_train = train[features], train[args.target]
    X_test, y_test = test[features], test[args.target]

    cv, groups = cv_scheme(args, train)
    if args.split == "time":  # TimeSeriesSplit expects rows in time order
        order = pd.to_datetime(train[args.time_col], errors="coerce").sort_values(kind="mergesort").index
        X_train, y_train = X_train.loc[order], y_train.loc[order]

    results = {}
    for name, model in build_models(args.task, numeric, categorical).items():
        scores = cross_val_score(model, X_train, y_train, cv=cv, groups=groups, scoring=metric, n_jobs=-1)
        results[name] = {"cv_mean": float(scores.mean()), "cv_std": float(scores.std()), "folds": scores.round(4).tolist()}
        print(f"  {name:24} CV {metric}: {scores.mean():.4f} +/- {scores.std():.4f}")

    candidates = {k: v for k, v in results.items() if not k.startswith("baseline")}
    best_name = max(candidates, key=lambda k: candidates[k]["cv_mean"])
    baseline = next(v for k, v in results.items() if k.startswith("baseline"))
    print(f"Selected {best_name} (baseline CV {baseline['cv_mean']:.4f})")

    best = build_models(args.task, numeric, categorical)[best_name].fit(X_train, y_train)
    # Test set: used once, after model selection.
    from sklearn.metrics import get_scorer
    test_score = float(get_scorer(metric)(best, X_test, y_test))
    print(f"Locked test {metric}: {test_score:.4f} on {len(test)} rows")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    preds = pd.DataFrame({"y_true": y_test.to_numpy()})
    if args.task == "classification":
        preds["y_pred"] = best.predict(X_test)
        if hasattr(best, "predict_proba") and y_train.nunique() == 2:
            preds["y_score"] = best.predict_proba(X_test)[:, 1]
    else:
        preds["y_pred"] = best.predict(X_test)
    for col in (args.group_col, args.time_col):
        if col and col in test.columns:
            preds[col] = test[col].to_numpy()
    preds.to_csv(out / "test_predictions.csv", index=False)

    metadata = {
        "model_name": best_name, "task": args.task, "target": args.target, "metric": metric,
        "features": features, "numeric_features": numeric, "categorical_features": categorical,
        "dtypes": {c: str(df[c].dtype) for c in features},
        "classes": [str(c) for c in sorted(y_train.unique())] if args.task == "classification" else None,
        "cv_results": results, "test_score": test_score, "train_rows": len(train), "test_rows": len(test),
        "split": args.split, "time_col": args.time_col, "group_col": args.group_col,
        "data_sha256": hashlib.sha256(raw_bytes).hexdigest(), "git_commit": git_commit(),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "versions": {"python": platform.python_version(), "sklearn": sklearn.__version__, "pandas": pd.__version__, "numpy": np.__version__},
        "seed": SEED,
    }
    joblib.dump(best, out / "model.joblib")
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    print(f"Saved model, metadata, and test predictions to {out}")

    if args.mlflow:
        try:
            import mlflow
            from mlflow.models import infer_signature
        except ImportError:
            print("MLflow not installed; skipped tracking (pip install mlflow).", file=sys.stderr)
        else:
            mlflow.set_experiment(args.experiment)
            with mlflow.start_run(run_name=best_name):
                mlflow.log_params({"model": best_name, "split": args.split, "folds": args.folds, "metric": metric,
                                   "n_features": len(features), "data_sha256": metadata["data_sha256"][:16]})
                for name, res in results.items():
                    mlflow.log_metric(f"cv_{name}", res["cv_mean"])
                mlflow.log_metric("test_score", test_score)
                mlflow.sklearn.log_model(best, name="model", signature=infer_signature(X_test.head(100), best.predict(X_test.head(100))),
                                         input_example=X_test.head(5))
                mlflow.log_artifact(str(out / "metadata.json"))
            print("Logged run to MLflow.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
