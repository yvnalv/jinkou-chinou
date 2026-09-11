# EDA Checklist

Detailed checks for steps 3–6 of the workflow. Use what applies; mark the rest N/A in your head, not in the report.

## Contents

1. Structure and grain
2. Data-quality dimensions
3. Checks by column kind
4. Missing-data analysis
5. Outliers
6. Relationships
7. Time-based data
8. Target and leakage
9. Common pitfalls
10. Severity and the cleaning plan

---

## 1. Structure and grain

- [ ] State the grain in one sentence: "one row = one order line per day".
- [ ] Candidate key(s): unique and never null. Check composite keys when no single column is unique: `df.duplicated(subset=[...]).sum()`.
- [ ] Exact duplicate rows: count them, inspect a few, and decide whether they are errors or legitimate repeats.
- [ ] Duplicate IDs with different attribute values: this is a conflict, not a duplicate. Show which columns differ.
- [ ] Row count and time coverage match expectations (a month of data with 3 days missing is a finding).
- [ ] Columns match the data dictionary: missing, extra, renamed, or shifted columns (a header off by one shows as every column holding the neighbour's values).
- [ ] Hierarchies are consistent: a city always maps to the same country, a product to one category.

## 2. Data-quality dimensions

| Dimension | Question | Typical checks |
|---|---|---|
| Completeness | Is anything missing? | Null counts per column and per row; disguised nulls; missing periods or segments |
| Uniqueness | Is anything repeated that should not be? | Duplicate rows, duplicate keys, near-duplicates (case, whitespace, typos) |
| Validity | Do values follow the rules? | Types, formats (email, phone, postcode), allowed ranges and category sets, units |
| Consistency | Do values agree with each other? | Start ≤ end, totals = sum of parts, same entity with conflicting attributes, cross-column logic |
| Plausibility | Are values realistic? | Ages 0–120, no negative prices or quantities unless refunds, no future birth dates |
| Timeliness | Is the data current and continuous? | Latest timestamp versus expected, lag, gaps, sudden volume changes |

## 3. Checks by column kind

**Numeric**

- [ ] min, max, mean, median, standard deviation, and 1st/99th percentiles. Is the range plausible?
- [ ] Skew: if strongly skewed, describe it with the median and IQR, and view it on a log scale.
- [ ] Zeros and negatives: meaningful, or codes for unknown?
- [ ] Sentinels: -1, 0, 99, 999, 9999 appearing much more often than neighbouring values.
- [ ] Integer-valued floats: often an integer column that contains nulls.
- [ ] Heaping: spikes at round numbers (10, 50, 100) suggest estimates or manual entry.
- [ ] Units: mixed scales in one column (grams and kilograms, cents and dollars) show as a bimodal distribution with a ratio of about 1000 or 100.

**Categorical**

- [ ] Frequencies and share of the top levels; count of rare levels (for example below 1%).
- [ ] Variants of the same value: case, whitespace, spelling, abbreviations ("Jakarta", "jakarta ", "JKT").
- [ ] Unexpected levels compared with the documented set.
- [ ] High cardinality: group rare levels or choose a suitable encoding later.
- [ ] Levels that are really missing ("Unknown", "Other", "-", "N/A").

**Datetime**

- [ ] Parse success rate and format; day/month order for ambiguous formats (03/04/2024).
- [ ] Time zone: naive or aware, mixed zones, daylight-saving jumps.
- [ ] Range: future dates, dates before the system existed, placeholder dates (1900-01-01, 1970-01-01, 9999-12-31).
- [ ] Volume per day, week, or month: gaps, spikes, and the partial first and last periods.
- [ ] Order constraints between date columns (created ≤ updated ≤ closed).

**Text**

- [ ] Length distribution; empty and whitespace-only strings.
- [ ] Encoding problems (mojibake such as `Ã©`), HTML remnants, line breaks inside fields.
- [ ] Language and structure: free text versus semi-structured content that should be parsed.
- [ ] Personal data inside free text.

**Boolean**

- [ ] Representations (1/0, Y/N, yes/no, true/false, ya/tidak) and whether they are mixed.
- [ ] Balance, and whether null means false or unknown.

**Identifier**

- [ ] Uniqueness at the stated grain; format consistency (length, prefix, check digits).
- [ ] Leading zeros preserved; long numeric IDs not converted to floats or scientific notation.
- [ ] Never use it as a numeric feature. Check whether it encodes time or source (sequential IDs often do).

## 4. Missing-data analysis

1. Quantify: count and percentage per column, and the distribution of missing values per row.
2. Pattern: which columns go missing together (`df.isna().corr()` or a missingness heatmap on a sample).
3. Relation to other data: does missingness vary by segment, source, or period, or with the target? Compare the target rate between rows with and without the value.
4. Mechanism, in practical terms:
   - **Random-looking** (unrelated to anything observed): dropping or simple imputation is usually safe.
   - **Explained by other columns** (for example one source system never fills it): impute using those columns, or model by segment.
   - **Related to the value itself** (high incomes left blank): the fact that it is missing is information. Keep an indicator and say so.
5. Record a proposed treatment per column; do not apply it during EDA.

## 5. Outliers

| Method | Use when |
|---|---|
| IQR fences (Q1 − 1.5·IQR, Q3 + 1.5·IQR) | Quick screen on roughly symmetric data. It flags too much on skewed data, so screen on the log scale there. |
| Robust z-score using the median and MAD (\|z\| > 3.5) | Skewed or heavy-tailed data |
| Domain limits | Always, when known: age 0–120, percentage 0–100, non-negative counts |
| Multivariate view (scatter plot, ratio checks) | Values plausible alone but not together (height 2 m and weight 20 kg) |

Decide per case:

| Finding | Action to propose |
|---|---|
| Impossible value (data-entry or system error) | Set to missing, or correct from the source |
| Placeholder or sentinel | Recode to missing (keep an indicator if informative) |
| Real but extreme | Keep. Consider a robust statistic, a transformation, or capping for specific models, and say which |
| Different population (test accounts, internal users) | Filter with a documented rule |

## 6. Relationships

| Pair | Look at | Measure |
|---|---|---|
| numeric–numeric | Scatter plot (sampled, with transparency) or hexbin | Pearson (linear), Spearman (monotonic) |
| categorical–numeric | Box or violin plot per level, group means and medians with counts | Correlation ratio (η) |
| categorical–categorical | Crosstab with row percentages, stacked bars | Cramér's V |
| any–time | Line chart per period, per segment | Trend and seasonality by eye; period-over-period change |

- [ ] Redundant pairs (\|r\| ≥ 0.9): derived columns, unit copies, totals and their parts.
- [ ] Surprising strong or absent relationships relative to domain knowledge: both are findings.
- [ ] Confounding: check whether a relationship holds within segments (see Simpson's paradox below).
- [ ] With many comparisons some will look significant by chance. Treat findings from broad scanning as hypotheses.

## 7. Time-based data

- [ ] Coverage: first and last timestamps, missing periods, partial periods at the edges.
- [ ] Volume over time: sudden level shifts often mean a system, definition, or tracking change rather than real behaviour.
- [ ] Trend and seasonality (day of week, month, holidays, including local ones such as Lebaran or Christmas).
- [ ] Drift: compare distributions of key columns between an early and a late period.
- [ ] Late-arriving data: the most recent periods may be incomplete.
- [ ] For later modeling, splits must respect time (train on the past, validate on the future).

## 8. Target and leakage

- [ ] Target definition: how and when it is recorded, and at what grain.
- [ ] Missing target values, and why they are missing.
- [ ] Classification: class balance, minority-class share, and balance over time and by segment.
- [ ] Regression: distribution, skew, zeros, extreme values; consider whether a log target makes sense.
- [ ] Leakage review, for every feature that is strongly associated with the target (strength ≥ 0.8 deserves a look, ≥ 0.95 is a red flag):
  - Is it known **before** the moment the prediction would be made?
  - Is it computed from the target, or updated after the outcome (status fields, "days since cancellation")?
  - Does an ID, timestamp, or file source encode the label?
  - Would duplicates of the same entity end up in both train and test?
- [ ] Record features to exclude and why.

## 9. Common pitfalls

| Pitfall | What goes wrong | Guard |
|---|---|---|
| pandas default NA parsing | "NA" (North America, Namibia) and "null" silently become missing | Rerun with `--raw-na`; compare null counts |
| Day/month ambiguity | 03/04 read as March 4 instead of 3 April | Check the ambiguous-date flag; confirm with values above 12 |
| Excel damage | Leading zeros lost, long IDs in scientific notation, codes turned into dates ("MAR1" → 1-Mar) | Read IDs and codes as text; inspect the raw file |
| Encoding | Mojibake in names; the file is not UTF-8 | Pass the right `--encoding` (cp1252, latin-1) |
| Float precision | Money sums off by cents; IDs above 2^53 corrupted | Read IDs as strings; use decimals or integer cents for money |
| Mixed units or currencies | Averages are meaningless | Check bimodality and the ratio between modes; look for a unit column |
| Time zones | Events shift across midnight; daily counts distorted | Normalize to one zone and state which |
| Simpson's paradox | A trend reverses within every segment | Check key relationships within major segments |
| Survivorship and selection bias | The data only contains customers who stayed, or successful transactions | Ask how rows enter the dataset; compare with the known population |
| Wrong aggregation level | Averages of averages; per-row metrics on duplicated joins | Recompute from the base grain; check row counts after joins |
| Sampling artefacts | A head-of-file sample is ordered by date or source | Use a random sample (`--sample`, not `--nrows`) |

## 10. Severity and the cleaning plan

| Severity | Meaning |
|---|---|
| High | Makes results wrong or unsafe if ignored: wrong grain, leakage, target problems, personal data exposure, large systematic missingness, corrupted keys |
| Medium | Biases or weakens results: moderate missingness, inconsistent categories, sentinels, type problems, many outliers |
| Low | Cosmetic or easily handled later: whitespace, mild skew, high cardinality, IDs to drop |

Cleaning plan rows (in the report, in execution order):

| Step | Issue | Action | Rows affected | Rationale | Reversible? |
|---|---|---|---|---|---|
| 1 | DQ-003 | Recode age = -1 to missing | 40 (2.0%) | -1 is a sentinel for unknown | Yes, the raw file is kept |

Apply steps only after the user approves them, in code, and rerun the profile on the cleaned output to confirm.
