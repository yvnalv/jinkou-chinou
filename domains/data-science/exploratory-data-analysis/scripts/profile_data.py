#!/usr/bin/env python3
"""Profile a tabular dataset as the first pass of exploratory data analysis.

Produces a JSON profile: source details, shape, duplicate rows, candidate keys,
per-column statistics with an inferred kind (numeric, categorical, datetime,
boolean, identifier, text, constant, empty), high correlations, optional
associations with a target column, and a ranked list of data-quality issues.

With --out, the full JSON is written to that file and a short text summary is
printed instead. The input file is never modified.

Values in columns that look like personal data (emails, phones, names, IDs) are
masked in the output unless --show-values is given.

Requires pandas and numpy. Parquet needs pyarrow; Excel needs openpyxl.

Examples:
  python profile_data.py data/sales.csv
  python profile_data.py data/sales.csv --target churned --out eda/profile.json
  python profile_data.py big.csv --sample 200000 --seed 42 --dayfirst
  python profile_data.py book.xlsx --sheet Orders
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import random
import re
import sys
import warnings
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover - depends on the environment
    sys.exit("profile_data.py needs pandas and numpy. Install them with: pip install pandas numpy")

warnings.filterwarnings("ignore")

TEXT_EXTENSIONS = {".csv", ".tsv", ".tab", ".txt"}
JSON_LINES_EXTENSIONS = {".jsonl", ".ndjson"}
MASK = "***masked***"
NULL_TOKENS = {"", "null", "none", "nan", "n/a", "na", "#n/a", "-", "--", "?", "missing", "undefined", "nil"}
BOOL_WORDS = {"0", "1", "true", "false", "t", "f", "yes", "no", "y", "n", "ya", "tidak"}
SENTINELS = {-1.0, -9.0, -99.0, -999.0, -9999.0, 999.0, 9999.0, 99999.0, 999999.0}
PII_TOKENS = {
    "email", "mail", "phone", "mobile", "handphone", "nohp", "telp", "telepon", "whatsapp", "wa",
    "ssn", "nik", "ktp", "passport", "paspor", "address", "alamat", "dob", "birthdate", "birthday",
    "lahir", "iban", "npwp", "ip", "firstname", "lastname", "fullname", "surname", "nama",
}
NAME_QUALIFIERS = {"first", "last", "full", "customer", "user", "contact", "patient", "employee", "person", "client", "member"}
ID_TOKENS = {"id", "uuid", "guid", "key", "code", "no", "number", "nr", "ref"}
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PHONE_RE = re.compile(r"^\+?[\d\s\-().]{9,20}$")
IPV4_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
DATE_HINT_RE = re.compile(r"[-/:]|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", re.I)
AMBIGUOUS_DATE_RE = re.compile(r"^\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}")
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def num(value, digits: int = 6):
    """Convert numpy/pandas scalars to JSON-safe Python values."""
    if value is None:
        return None
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        f = float(value)
        return None if math.isnan(f) or math.isinf(f) else round(f, digits)
    if isinstance(value, (pd.Timestamp, dt.datetime, dt.date)):
        return None if pd.isna(value) else value.isoformat()
    return value


def short(value, limit: int = 80) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def pct(part: float, whole: float) -> float | None:
    return round(100.0 * part / whole, 3) if whole else None


def name_tokens(column: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(column))
    return [t for t in re.split(r"[^A-Za-z0-9]+", spaced.lower()) if t]


def luhn_ok(digits: str) -> bool:
    total, parity = 0, len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def looks_like_phone(text: str) -> bool:
    if not PHONE_RE.match(text):
        return False
    digits = re.sub(r"\D", "", text)
    return 9 <= len(digits) <= 15 and (text.startswith(("+", "0")) or bool(re.search(r"[\s\-().]", text)))


def looks_like_card(text: str) -> bool:
    digits = re.sub(r"[\s-]", "", text)
    return digits.isdigit() and 13 <= len(digits) <= 19 and luhn_ok(digits)


def pii_reason(column: str, strings: pd.Series | None) -> str | None:
    tokens = name_tokens(column)
    if any(t in PII_TOKENS for t in tokens):
        return "column name suggests personal data"
    if "name" in tokens and (len(tokens) == 1 or any(t in NAME_QUALIFIERS for t in tokens)):
        return "column name suggests personal names"
    if strings is not None and len(strings):
        sample = strings.sample(min(len(strings), 500), random_state=0).str.strip()
        checks = {
            "email addresses": sample.str.match(EMAIL_RE),
            "phone numbers": sample.map(looks_like_phone),
            "IP addresses": sample.str.match(IPV4_RE),
            "payment card numbers": sample.map(looks_like_card),
        }
        for label, hits in checks.items():
            if hits.mean() >= 0.3:
                return f"values look like {label}"
    return None


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def detect_encoding(path: Path) -> str:
    raw = path.open("rb").read(1 << 20)
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        raw[:-4].decode("utf-8") if len(raw) == 1 << 20 else raw.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def sniff_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, errors="replace", newline="") as fh:
        sample = fh.read(65536)
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def count_data_lines(path: Path) -> int:
    with path.open("rb") as fh:
        lines = sum(chunk.count(b"\n") for chunk in iter(lambda: fh.read(1 << 20), b""))
    return max(lines - 1, 0)


def load(args: argparse.Namespace) -> tuple[pd.DataFrame, dict, list[str]]:
    path = Path(args.path)
    if not path.is_file():
        sys.exit(f"error: file not found: {path}")
    ext = path.suffix.lower()
    notes: list[str] = []
    source = {
        "path": str(path),
        "format": ext.lstrip(".") or "unknown",
        "size_bytes": path.stat().st_size,
        "sampled": False,
        "sample_method": None,
        "rows_in_file": None,
    }
    try:
        if ext in TEXT_EXTENSIONS:
            encoding = args.encoding or detect_encoding(path)
            sep = args.sep or ("\t" if ext in {".tsv", ".tab"} else sniff_delimiter(path, encoding))
            source.update(encoding=encoding, delimiter=sep)
            if encoding == "latin-1" and not args.encoding:
                notes.append("File is not valid UTF-8; read as latin-1. Pass --encoding if characters look wrong.")
            # Read as raw strings so leading zeros, disguised missing values and
            # mixed types stay visible; types are inferred per column afterwards.
            kwargs = {"sep": sep, "encoding": encoding, "dtype": str, "keep_default_na": not args.raw_na}
            if args.raw_na:
                kwargs["na_values"] = [""]
            if args.nrows:
                kwargs["nrows"] = args.nrows
                source.update(sampled=True, sample_method=f"first {args.nrows} rows")
            elif args.sample:
                total = count_data_lines(path)
                source["rows_in_file"] = total
                if total > args.sample:
                    rng = random.Random(args.seed)
                    keep = args.sample / total
                    kwargs["skiprows"] = lambda i: i > 0 and rng.random() > keep
                    source.update(sampled=True, sample_method=f"random ~{args.sample} of {total} rows (seed {args.seed})")
            df = pd.read_csv(path, **kwargs)
        elif ext in {".parquet", ".pq"}:
            df = pd.read_parquet(path)
        elif ext in {".xlsx", ".xlsm", ".xls"}:
            sheets = pd.ExcelFile(path).sheet_names
            sheet = args.sheet if args.sheet is not None else sheets[0]
            source.update(sheet=sheet, sheets=sheets)
            if len(sheets) > 1 and args.sheet is None:
                notes.append(f"Workbook has {len(sheets)} sheets; profiled '{sheet}'. Use --sheet for the others.")
            df = pd.read_excel(path, sheet_name=sheet, nrows=args.nrows)
        elif ext in JSON_LINES_EXTENSIONS:
            df = pd.read_json(path, lines=True, nrows=args.nrows)
        elif ext == ".json":
            df = pd.read_json(path)
        elif ext == ".feather":
            df = pd.read_feather(path)
        else:
            sys.exit(f"error: unsupported file type '{ext}' (csv, tsv, txt, parquet, xlsx, xls, json, jsonl, feather)")
    except ImportError as exc:
        sys.exit(f"error: {exc}. Parquet needs 'pip install pyarrow'; Excel needs 'pip install openpyxl'.")

    if not source["sampled"] and args.sample and len(df) > args.sample:
        source["rows_in_file"] = len(df)
        df = df.sample(n=args.sample, random_state=args.seed)
        source.update(sampled=True, sample_method=f"random {args.sample} of {source['rows_in_file']} rows (seed {args.seed})")
    if source["rows_in_file"] is None and not source["sampled"]:
        source["rows_in_file"] = len(df)
    df.columns = [str(c) for c in df.columns]
    return df, source, notes


# ---------------------------------------------------------------------------
# Column profiling
# ---------------------------------------------------------------------------

def parse_dates(strings: pd.Series, dayfirst: bool) -> pd.Series:
    try:
        return pd.to_datetime(strings, errors="coerce", format="mixed", dayfirst=dayfirst)
    except (TypeError, ValueError):
        return pd.to_datetime(strings, errors="coerce", dayfirst=dayfirst)


def coerce_text_column(s: pd.Series, dayfirst: bool) -> tuple[pd.Series, dict]:
    """Detect numbers or dates stored as text and convert them for profiling."""
    info: dict = {}
    strings = s.dropna().astype(str).str.strip()
    strings = strings[~strings.str.lower().isin(NULL_TOKENS)]
    if strings.empty:
        return s, info
    numeric = pd.to_numeric(strings.str.replace(r"^\+", "", regex=True), errors="coerce")
    numeric_share = numeric.notna().mean()
    if numeric_share >= 0.95:
        leading_zero = strings.str.match(r"^0\d").mean()
        if leading_zero >= 0.05:
            info["leading_zero_codes"] = True
            return s, info
        info["converted_from_text"] = "numeric"
        bad = strings[numeric.isna()].unique()[:5]
        info["unparseable_examples"] = [short(b) for b in bad]
        converted = pd.to_numeric(s.astype(str).str.strip().str.replace(r"^\+", "", regex=True), errors="coerce")
        return converted.where(s.notna()), info
    hinted = strings[strings.str.contains(DATE_HINT_RE)]
    if len(hinted) >= 0.95 * len(strings):
        probe = hinted.sample(min(len(hinted), 1000), random_state=0)
        if parse_dates(probe, dayfirst).notna().mean() >= 0.95:
            info["converted_from_text"] = "datetime"
            parsed = parse_dates(s.astype(str).str.strip(), dayfirst)
            bad = strings[parse_dates(strings, dayfirst).isna()].unique()[:5]
            info["unparseable_examples"] = [short(b) for b in bad]
            return parsed.where(s.notna()), info
    return s, info


def infer_kind(column: str, s: pd.Series, nunique: int, non_null: int) -> str:
    if non_null == 0:
        return "empty"
    if nunique == 1:
        return "constant"
    if pd.api.types.is_bool_dtype(s):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(s):
        return "datetime"
    if pd.api.types.is_timedelta64_dtype(s):
        return "timedelta"
    tokens = name_tokens(column)
    id_name = any(t in ID_TOKENS for t in tokens) or column.lower().endswith("id")
    if pd.api.types.is_numeric_dtype(s):
        if nunique == 2:
            return "boolean"
        values = s.dropna()
        integer_valued = bool((values == values.round()).all())
        if id_name and integer_valued and nunique / non_null > 0.95:
            return "identifier"
        return "numeric"
    strings = s.dropna().astype(str)
    if nunique == 2 and set(strings.str.strip().str.lower().unique()) <= BOOL_WORDS:
        return "boolean"
    unique_ratio = nunique / non_null
    avg_len = strings.str.len().mean()
    if unique_ratio > 0.95 and non_null > 20:
        return "text" if avg_len > 40 else "identifier"
    if avg_len > 40 and unique_ratio > 0.5:
        return "text"
    return "categorical"


def top_values(s: pd.Series, n: int, masked: bool) -> list[dict]:
    counts = s.value_counts(dropna=True).head(n)
    total = int(s.notna().sum())
    return [
        {"value": MASK if masked else short(v), "count": int(c), "pct": pct(c, total)}
        for v, c in counts.items()
    ]


def numeric_stats(s: pd.Series) -> dict:
    x = s.dropna().astype(float)
    if x.empty:
        return {}
    q = x.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    iqr = q[0.75] - q[0.25]
    lo, hi = q[0.25] - 1.5 * iqr, q[0.75] + 1.5 * iqr
    outliers = int(((x < lo) | (x > hi)).sum()) if iqr > 0 else 0
    counts = x.value_counts()
    sentinels = [
        {"value": num(v), "count": int(counts[v]), "pct": pct(counts[v], len(x))}
        for v in counts.index if v in SENTINELS and counts[v] / len(x) >= 0.01
    ]
    return {
        "min": num(x.min()), "max": num(x.max()), "mean": num(x.mean()), "std": num(x.std()),
        "p01": num(q[0.01]), "p05": num(q[0.05]), "p25": num(q[0.25]), "median": num(q[0.5]),
        "p75": num(q[0.75]), "p95": num(q[0.95]), "p99": num(q[0.99]),
        "skew": num(x.skew(), 3), "kurtosis": num(x.kurt(), 3),
        "zeros": int((x == 0).sum()), "negatives": int((x < 0).sum()),
        "integer_valued": bool((x == x.round()).all()),
        "outliers_iqr": outliers, "outliers_pct": pct(outliers, len(x)),
        "iqr_fences": [num(lo), num(hi)],
        "sentinel_candidates": sentinels,
    }


def datetime_stats(s: pd.Series) -> dict:
    x = s.dropna()
    if x.empty:
        return {}
    if getattr(x.dt, "tz", None) is not None:
        x = x.dt.tz_convert(None)
    now = pd.Timestamp.now()
    return {
        "min": num(x.min()), "max": num(x.max()),
        "span_days": num((x.max() - x.min()).total_seconds() / 86400, 2),
        "future_values": int((x > now).sum()),
        "before_1900": int((x < pd.Timestamp("1900-01-01")).sum()),
        "has_time_component": bool((x.dt.normalize() != x).any()),
        "rows_per_year": {str(k): int(v) for k, v in x.dt.year.value_counts().sort_index().items()},
    }


def text_stats(s: pd.Series) -> dict:
    strings = s.dropna().astype(str)
    if strings.empty:
        return {}
    lengths = strings.str.len()
    stripped = strings.str.strip()
    normalized = stripped.str.lower().str.replace(r"\s+", " ", regex=True)
    null_like = strings[stripped.str.lower().isin(NULL_TOKENS)]
    return {
        "length_min": int(lengths.min()), "length_mean": num(lengths.mean(), 2), "length_max": int(lengths.max()),
        "leading_trailing_whitespace": int((strings != stripped).sum()),
        "null_like_values": int(len(null_like)),
        "null_like_examples": sorted({repr(v) for v in null_like.unique()[:5]}),
        "case_or_space_variants": int(strings.nunique() - normalized.nunique()),
    }


def profile_column(df: pd.DataFrame, column: str, args: argparse.Namespace, text_source: bool) -> tuple[dict, pd.Series]:
    raw = df[column]
    rows = len(raw)
    s, conversion = raw, {}
    is_text = raw.dtype == object or pd.api.types.is_string_dtype(raw)
    if is_text:
        s, conversion = coerce_text_column(raw, args.dayfirst)
        if conversion.get("converted_from_text"):
            # In CSV-like files every value is text, so conversion alone is not a problem.
            conversion["text_source"] = text_source
        if conversion.get("converted_from_text") == "datetime":
            sample = raw.dropna().astype(str).str.strip().head(1000)
            conversion["ambiguous_day_month"] = bool(sample.str.match(AMBIGUOUS_DATE_RE).any())
            conversion["dayfirst"] = args.dayfirst
    non_null = int(s.notna().sum())
    nunique = int(s.nunique(dropna=True))
    kind = infer_kind(column, s, nunique, non_null)
    strings = raw.dropna().astype(str) if is_text else None
    reason = pii_reason(column, strings)
    masked = bool(reason) and not args.show_values

    info = {
        "name": column,
        "dtype": str(s.dtype),
        "kind": kind,
        "non_null": non_null,
        "missing": rows - non_null,
        "missing_pct": pct(rows - non_null, rows),
        "unique": nunique,
        "unique_pct": pct(nunique, non_null),
        "top_values": top_values(s if kind != "datetime" else s.dt.strftime("%Y-%m-%d"), args.top, masked),
    }
    if conversion:
        info["conversion"] = conversion
    if reason:
        info["pii_suspected"] = reason
    if kind == "numeric":
        info["numeric"] = numeric_stats(s)
    elif kind == "datetime":
        info["datetime"] = datetime_stats(s)
    if is_text and kind in {"categorical", "text", "identifier", "boolean"}:
        info["text"] = text_stats(raw)
        if masked:
            info["text"]["null_like_examples"] = []
    if conversion.get("unparseable_examples") and masked:
        conversion["unparseable_examples"] = [MASK]
    return info, s


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

def limit_categories(s: pd.Series, top: int = 50) -> pd.Series:
    keep = s.value_counts().head(top).index
    return s.where(s.isin(keep) | s.isna(), "__other__")


def correlation_ratio(categories: pd.Series, values: pd.Series) -> float | None:
    frame = pd.DataFrame({"c": categories, "v": values}).dropna()
    if len(frame) < 3 or frame["v"].var() == 0:
        return None
    grand = frame["v"].mean()
    groups = frame.groupby("c", observed=True)["v"]
    between = float((groups.count() * (groups.mean() - grand) ** 2).sum())
    total = float(((frame["v"] - grand) ** 2).sum())
    return math.sqrt(between / total) if total else None


def cramers_v(a: pd.Series, b: pd.Series) -> float | None:
    table = pd.crosstab(a, b)
    if table.shape[0] < 2 or table.shape[1] < 2:
        return None
    observed = table.to_numpy(dtype=float)
    n = observed.sum()
    expected = np.outer(observed.sum(axis=1), observed.sum(axis=0)) / n
    chi2 = float(((observed - expected) ** 2 / expected).sum())
    k = min(table.shape) - 1
    return math.sqrt(chi2 / (n * k)) if n and k else None


def high_correlations(numeric: pd.DataFrame, threshold: float) -> dict:
    if numeric.shape[1] < 2:
        return {"method": "pearson and spearman", "threshold": threshold, "pairs": [], "columns_used": numeric.shape[1]}
    truncated = numeric.shape[1] > 150
    if truncated:
        numeric = numeric[numeric.notna().sum().sort_values(ascending=False).index[:150]]
    pearson = numeric.corr(method="pearson")
    spearman = numeric.corr(method="spearman")
    pairs = []
    cols = list(numeric.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            p, r = pearson.loc[a, b], spearman.loc[a, b]
            if max(abs(p) if pd.notna(p) else 0, abs(r) if pd.notna(r) else 0) >= threshold:
                pairs.append({"a": a, "b": b, "pearson": num(p, 4), "spearman": num(r, 4)})
    pairs.sort(key=lambda d: -max(abs(d["pearson"] or 0), abs(d["spearman"] or 0)))
    return {"method": "pearson and spearman", "threshold": threshold, "pairs": pairs,
            "columns_used": len(cols), "truncated_to_150_columns": truncated}


def target_analysis(target: str, columns: dict[str, dict], series: dict[str, pd.Series]) -> dict:
    t_info = columns[target]
    t = series[target]
    kind = t_info["kind"]
    result: dict = {"column": target, "kind": kind, "missing": t_info["missing"], "missing_pct": t_info["missing_pct"]}
    is_categorical_target = kind in {"categorical", "boolean"} or (kind == "numeric" and t_info["unique"] <= 10)
    if is_categorical_target:
        counts = t.value_counts(dropna=True)
        result["task_hint"] = "classification"
        result["classes"] = [{"value": short(v), "count": int(c), "pct": pct(c, counts.sum())} for v, c in counts.head(20).items()]
        if len(counts) >= 2:
            result["imbalance_ratio"] = num(counts.iloc[0] / counts.iloc[-1], 2)
            result["minority_class_pct"] = pct(counts.iloc[-1], counts.sum())
    elif kind == "numeric":
        result["task_hint"] = "regression"
    else:
        result["task_hint"] = "unclear (target is not numeric or low-cardinality)"
        return result

    associations = []
    t_cat = limit_categories(t.astype("object")) if is_categorical_target else None
    for name, info in columns.items():
        if name == target or info["kind"] in {"identifier", "text", "constant", "empty", "timedelta"}:
            continue
        s = series[name]
        try:
            if info["kind"] == "numeric" and not is_categorical_target:
                value, method = s.corr(t, method="spearman"), "spearman"
            elif info["kind"] == "numeric":
                value, method = correlation_ratio(t_cat, s), "correlation_ratio"
            elif info["kind"] == "datetime":
                continue
            elif is_categorical_target:
                value, method = cramers_v(limit_categories(s.astype("object")), t_cat), "cramers_v"
            else:
                value, method = correlation_ratio(limit_categories(s.astype("object")), t), "correlation_ratio"
        except (TypeError, ValueError):
            continue
        if value is not None and pd.notna(value):
            associations.append({"feature": name, "method": method, "strength": num(abs(value), 4)})
    associations.sort(key=lambda d: -d["strength"])
    result["associations"] = associations[:30]
    result["note"] = "Association strength is 0..1 and not causal. Values near 1 often mean leakage or a duplicate of the target."
    return result


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

def collect_issues(profile: dict) -> list[dict]:
    issues: list[dict] = []

    def add(severity: str, column: str | None, code: str, detail: str) -> None:
        issues.append({"severity": severity, "column": column, "issue": code, "detail": detail})

    dup = profile["duplicates"]
    if dup["exact_duplicate_rows"]:
        add("high" if (dup["pct"] or 0) > 5 else "medium", None, "duplicate_rows",
            f"{dup['exact_duplicate_rows']} exact duplicate rows ({dup['pct']}%)")

    for c in profile["columns"]:
        name, kind = c["name"], c["kind"]
        if kind == "empty":
            add("high", name, "empty_column", "column has no values")
            continue
        if c["missing"]:
            mp = c["missing_pct"] or 0
            add("high" if mp > 50 else "medium" if mp > 5 else "low", name, "missing_values",
                f"{c['missing']} missing ({mp}%)")
        if kind == "constant":
            add("medium", name, "constant", "only one distinct value; carries no information")
        if kind == "identifier":
            add("low", name, "identifier", "looks like an ID; exclude from features, check uniqueness if it is a key")
        if c.get("pii_suspected"):
            add("high", name, "pii_suspected", f"{c['pii_suspected']}; values masked, handle per privacy rules")
        if kind == "identifier" and c["unique"] < c["non_null"]:
            dupes = c["non_null"] - c["unique"]
            add("medium", name, "duplicate_identifiers", f"{dupes} repeated ID values; check whether rows should be unique")
        conv = c.get("conversion", {})
        converted = conv.get("converted_from_text")
        bad = conv.get("unparseable_examples") or []
        if converted == "numeric" and bad:
            add("medium", name, "non_numeric_values", f"mostly numeric, but some values do not parse: {bad}")
        elif converted == "numeric" and not conv.get("text_source"):
            add("medium", name, "numeric_stored_as_text", "numbers stored as text; convert on load")
        if converted == "datetime" and bad:
            add("medium", name, "unparseable_dates", f"mostly dates, but some values do not parse: {bad}")
        elif converted == "datetime" and not conv.get("text_source"):
            add("low", name, "datetime_stored_as_text", "dates stored as text; parse on load")
        if converted == "datetime" and conv.get("ambiguous_day_month"):
            order = "day/month" if conv.get("dayfirst") else "month/day"
            add("low", name, "ambiguous_date_format",
                f"dates like 03/04/2024 were read as {order}; confirm (use --dayfirst to switch)")
        if conv.get("leading_zero_codes"):
            add("low", name, "leading_zero_codes", "numeric-looking codes with leading zeros; keep as text")
        text = c.get("text", {})
        if text.get("null_like_values"):
            add("medium", name, "disguised_missing",
                f"{text['null_like_values']} values like {text.get('null_like_examples') or 'null tokens'} should be missing")
        if text.get("case_or_space_variants"):
            add("medium", name, "inconsistent_categories",
                f"{text['case_or_space_variants']} distinct values collapse when case/whitespace is normalized")
        elif text.get("leading_trailing_whitespace"):
            add("low", name, "whitespace", f"{text['leading_trailing_whitespace']} values have leading/trailing spaces")
        if kind == "categorical" and c["unique"] > 50:
            add("low", name, "high_cardinality", f"{c['unique']} categories; group rare ones or use a suitable encoding")
        numeric = c.get("numeric", {})
        if numeric:
            op = numeric.get("outliers_pct") or 0
            if op > 1:
                add("medium" if op > 5 else "low", name, "outliers",
                    f"{numeric['outliers_iqr']} values ({op}%) outside IQR fences {numeric['iqr_fences']}")
            if numeric.get("skew") is not None and abs(numeric["skew"]) > 2:
                add("low", name, "skewed", f"skew {numeric['skew']}; consider a log/robust scale for analysis")
            for s in numeric.get("sentinel_candidates", []):
                add("medium", name, "sentinel_value", f"value {s['value']} appears {s['count']} times ({s['pct']}%); may encode missing")
        dates = c.get("datetime", {})
        if dates.get("future_values"):
            add("medium", name, "future_dates", f"{dates['future_values']} values are in the future")
        if dates.get("before_1900"):
            add("medium", name, "implausible_old_dates", f"{dates['before_1900']} values are before 1900")

    for pair in profile["correlations"]["pairs"]:
        strength = max(abs(pair["pearson"] or 0), abs(pair["spearman"] or 0))
        add("medium" if strength >= 0.98 else "low", f"{pair['a']} / {pair['b']}", "high_correlation",
            f"correlation {strength}; redundant features or derived columns")

    target = profile.get("target")
    if target:
        if target["missing"]:
            add("high", target["column"], "target_missing", f"{target['missing']} rows have no target value")
        if (target.get("minority_class_pct") or 100) < 5:
            add("medium", target["column"], "class_imbalance",
                f"minority class is {target['minority_class_pct']}% of rows; use stratified splits and suitable metrics")
        for a in target.get("associations", []):
            if a["strength"] >= 0.95:
                add("high", a["feature"], "leakage_suspect",
                    f"{a['method']} {a['strength']} with the target; check whether it is known before the outcome")

    issues.sort(key=lambda i: (SEVERITY_ORDER[i["severity"]], str(i["column"])))
    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_profile(args: argparse.Namespace) -> dict:
    df, source, notes = load(args)
    rows = len(df)
    text_source = "." + source["format"] in TEXT_EXTENSIONS
    columns: dict[str, dict] = {}
    series: dict[str, pd.Series] = {}
    for column in df.columns:
        columns[column], series[column] = profile_column(df, column, args, text_source)
    if text_source and not args.raw_na:
        notes.append("Tokens such as NA, N/A, null, NaN and empty fields were read as missing (pandas default). "
                     "Use --raw-na if any of them is a real value, e.g. NA = North America.")

    duplicates = int(df.duplicated().sum()) if rows else 0
    candidate_keys = [
        name for name, c in columns.items()
        if rows and c["missing"] == 0 and c["unique"] == rows and c["kind"] not in {"numeric", "text"}
    ][:10]
    numeric_frame = pd.DataFrame({n: series[n] for n, c in columns.items() if c["kind"] == "numeric"})

    if args.target and args.target not in columns:
        sys.exit(f"error: target column '{args.target}' not found. Columns: {', '.join(columns)}")

    profile = {
        "tool": "profile_data.py",
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "shape": {"rows": rows, "columns": len(columns)},
        "memory_mb": round(float(df.memory_usage(deep=True).sum()) / 1e6, 2),
        "duplicates": {"exact_duplicate_rows": duplicates, "pct": pct(duplicates, rows)},
        "candidate_keys": candidate_keys,
        "kinds": pd.Series([c["kind"] for c in columns.values()]).value_counts().to_dict() if columns else {},
        "columns": list(columns.values()),
        "correlations": high_correlations(numeric_frame, args.corr_threshold),
        "target": target_analysis(args.target, columns, series) if args.target else None,
        "notes": notes,
    }
    if source["sampled"]:
        notes.append(f"Statistics describe a sample ({source['sample_method']}); counts are not totals for the whole file.")
    if not args.show_values and any(c.get("pii_suspected") for c in columns.values()):
        notes.append("Values in columns suspected to hold personal data are masked. Use --show-values only when appropriate.")
    profile["issues"] = collect_issues(profile)
    return profile


def summary_text(profile: dict, out_path: str) -> str:
    shape, source = profile["shape"], profile["source"]
    counts = {s: sum(1 for i in profile["issues"] if i["severity"] == s) for s in SEVERITY_ORDER}
    lines = [
        f"Profiled {source['path']}: {shape['rows']:,} rows x {shape['columns']} columns"
        + (f" (sample: {source['sample_method']})" if source["sampled"] else ""),
        f"Kinds: {profile['kinds']}",
        f"Duplicate rows: {profile['duplicates']['exact_duplicate_rows']} ({profile['duplicates']['pct']}%)",
        f"Candidate keys: {profile['candidate_keys'] or 'none'}",
        f"Issues: {counts['high']} high, {counts['medium']} medium, {counts['low']} low",
    ]
    for issue in profile["issues"][:20]:
        lines.append(f"  {issue['severity'].upper():6} {issue['column'] or '(table)'}: {issue['issue']} - {issue['detail']}")
    if len(profile["issues"]) > 20:
        lines.append(f"  ... {len(profile['issues']) - 20} more in the JSON file")
    for note in profile["notes"]:
        lines.append(f"Note: {note}")
    lines.append(f"Full profile written to {out_path}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile a tabular dataset (CSV, TSV, Excel, Parquet, JSON) for exploratory data analysis.",
    )
    parser.add_argument("path", help="dataset file")
    parser.add_argument("--target", help="target/outcome column: adds class balance, associations, leakage checks")
    parser.add_argument("--sheet", help="Excel sheet name (default: first sheet)")
    parser.add_argument("--sep", help="delimiter for text files (default: sniffed)")
    parser.add_argument("--encoding", help="text encoding (default: utf-8, falling back to latin-1)")
    parser.add_argument("--sample", type=int, help="profile a random sample of about N rows")
    parser.add_argument("--nrows", type=int, help="read only the first N rows (quick look; biased)")
    parser.add_argument("--seed", type=int, default=42, help="random seed for --sample (default 42)")
    parser.add_argument("--dayfirst", action="store_true", help="parse ambiguous dates as day/month (e.g. 03/04 = 3 April)")
    parser.add_argument("--raw-na", action="store_true",
                        help="text files: treat only empty fields as missing (keep NA, N/A, null as values)")
    parser.add_argument("--top", type=int, default=5, help="top values to list per column (default 5)")
    parser.add_argument("--corr-threshold", type=float, default=0.9, help="report correlations at or above this (default 0.9)")
    parser.add_argument("--show-values", action="store_true", help="do not mask values in suspected personal-data columns")
    parser.add_argument("--out", help="write the full JSON here and print a short summary instead")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = parse_args(argv)
    profile = build_profile(args)
    text = json.dumps(profile, indent=2, ensure_ascii=False, default=str)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(summary_text(profile, str(out)))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
