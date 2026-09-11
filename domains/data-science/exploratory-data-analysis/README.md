# exploratory-data-analysis

Systematic profiling of a tabular dataset — structure and grain, data quality, distributions, relationships, and target leakage — ending in an evidence-backed `EDA_REPORT.md`, figures, a reproducible script, and a cleaning plan that waits for your approval. Raw data is never modified.

Domain: `data-science` · Type: `specialized`

## When to use

Invoke with `/exploratory-data-analysis`, or let Claude pick it up automatically when you ask for things like:

- "I just got `sales_2025.csv`, what's in it?"
- "Profile this Parquet file and tell me what's wrong with it."
- "Before we build a churn model, check `customers.xlsx` (target: `churned`)."
- "Audit this export from the finance system for data-quality problems."

It stops at understanding and a cleaning plan; modeling, dashboards, and pipelines are recommended as next steps, not done here.

### The profiler on its own

```text
python scripts/profile_data.py data.csv --out eda/profile.json --target churned
python scripts/profile_data.py big.csv --sample 200000 --seed 42
python scripts/profile_data.py book.xlsx --sheet Orders --dayfirst
python scripts/profile_data.py data.csv --raw-na        # keep NA / N/A / null as real values
```

Detects per column: kind (numeric, categorical, datetime, boolean, identifier, text, constant, empty), missing and disguised-missing values, numbers or dates stored as text, codes with leading zeros, case/whitespace variants, outliers (IQR), skew, sentinel values (-1, 999, …), future or implausible dates, suspected personal data (masked by default). Across columns: duplicate rows and IDs, candidate keys, high correlations, and — with `--target` — class balance, associations (Spearman, correlation ratio, Cramér's V), and leakage suspects.

## Structure

```text
exploratory-data-analysis/
├── SKILL.md                              # workflow, rules, definition of done
├── README.md
├── config/
│   └── skill.yaml                        # manifest + machine-readable policy
├── references/
│   ├── eda-checklist.md                  # quality dimensions, per-kind checks, missing data, outliers, leakage, pitfalls
│   ├── visualization-guide.md            # chart choice, standard figure set, plotting conventions
│   └── EDA_REPORT.template.md            # report structure
├── scripts/
│   └── profile_data.py                   # mechanical profile → JSON + ranked issue list
└── evals/
    └── evals.json                        # trigger and behavior test cases
```

Requirements: Python 3.10+, pandas 2.x, numpy, matplotlib (for figures); pyarrow for Parquet and openpyxl for Excel.

## Changelog

### 0.1.0 — 2026-09-10

- Initial version: 8-step workflow, profiler script (CSV/TSV/Excel/Parquet/JSON/Feather, sampling, target and leakage analysis, personal-data masking), checklist, visualization guide, and report template.
