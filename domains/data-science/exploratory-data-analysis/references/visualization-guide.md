# Visualization Guide for EDA

Charts in an EDA exist to answer questions and to show evidence for findings. Make fewer, clearer charts.

## Principles

1. **One question per chart.** The title states the finding when there is one ("Spend is right-skewed; median 20, p99 540"), otherwise the question.
2. **Label everything.** Axis labels with units, readable tick labels, and n in the subtitle or caption (for example "n = 2,010, 7.4% missing excluded").
3. **Honest scales.** Bar charts start at zero. Say when an axis is logarithmic. Do not truncate axes to exaggerate differences.
4. **Order with meaning.** Sort categories by frequency or by a natural order (months, sizes), not alphabetically by default. Group rare levels into "Other (k levels)".
5. **Accessible colour.** Use a colour-blind-safe palette (matplotlib `tab10` or seaborn `colorblind`), and do not rely on colour alone; add labels or markers.
6. **No chart junk.** No 3D, no pie charts with more than three slices, no dual axes unless unavoidable.
7. **No personal data.** Never plot raw names, emails, phone numbers, or IDs as labels.
8. **Big data.** Sample for scatter plots (random, stated), use transparency or hexbin, and aggregate time series to a sensible period.

## Which chart answers which question

| Question | Chart | Notes |
|---|---|---|
| How is a numeric variable distributed? | Histogram (+ box plot) | Choose bins deliberately; add a log-scale version when skew is above ~2 |
| What are the most common categories? | Horizontal bar chart of the top N with "Other" | Show percentages |
| Where is data missing? | Bar chart of missing % per column; missingness heatmap on a sample | Sort by missing % |
| Do two numeric variables move together? | Scatter plot or hexbin | Add a trend line only if it helps; state Pearson and Spearman |
| Does a numeric variable differ across groups? | Box or violin plot per group; point plot of means with intervals | Show n per group |
| Are two categorical variables related? | Heatmap of row percentages; 100% stacked bars | Row percentages, not raw counts |
| Which numeric variables are redundant? | Correlation heatmap (Spearman), clustered | Only with 3 or more numeric columns; annotate if fewer than ~15 |
| How does something change over time? | Line chart per period | Mark partial periods; one line per key segment at most ~5 |
| Is the target balanced? | Bar chart of class shares | Also over time if dates exist |
| How does a feature relate to the target? | Classification: target rate per bin or level. Regression: scatter or box plot | For the top associations and for leakage suspects |

## Standard EDA figure set

Produce what applies, in this order, and name the files with a number prefix so they sort:

1. `01_missing_by_column.png` — when any column has missing values.
2. `02_numeric_distributions.png` — small multiples of histograms for key numeric columns.
3. `03_top_categories_<column>.png` — for the important categorical columns.
4. `04_correlation_heatmap.png` — when there are at least 3 numeric columns.
5. `05_volume_over_time.png` — when there is a date column.
6. `06_target_balance.png` and `07_target_vs_<feature>.png` — when there is a target.

Add a chart beyond this set only when it supports a specific finding in the report.

## Code conventions

```python
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # render to files; works without a display
import matplotlib.pyplot as plt

FIG_DIR = Path("eda/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight")
    plt.close(fig)  # free memory when making many figures


# Example: missing values per column
missing = df.isna().mean().mul(100).sort_values()
missing = missing[missing > 0]
if not missing.empty:
    fig, ax = plt.subplots(figsize=(7, max(2, 0.3 * len(missing))))
    missing.plot.barh(ax=ax, color="#4C72B0")
    ax.set_xlabel("Missing (%)")
    ax.set_title(f"Missing values by column (n = {len(df):,} rows)")
    save(fig, "01_missing_by_column")
```

* Use matplotlib; seaborn is optional when it is already installed.
* Set `random_state` on any sampling used for plotting.
* Reference every saved figure from `EDA_REPORT.md` with a one-line takeaway under it.
