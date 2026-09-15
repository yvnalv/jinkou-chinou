# Mining Run Report: [Target Name / Batch ID]

*Date: [YYYY-MM-DD] | Status: [Completed / Partial / Failed] | Executed by: [/the-miner]*

---

## 1. Run Summary & Execution Metrics

| Metric | Measured Value | Target / Threshold |
|---|---|---|
| **Target Origin** | `[https://example.com]` | - |
| **Total URLs Attempted** | `[e.g., 5,000]` | `[5,000]` |
| **Successful Extractions** | `[e.g., 4,920 (98.4%)]` | `>= 95%` |
| **HTTP Errors (4xx/5xx)** | `[e.g., 18 (0.36%)]` | `< 2%` |
| **Anti-Bot Challenge Count** | `[e.g., 4 challenges encountered, 4 resolved]` | - |
| **Proxy Pool Health** | `[e.g., 50 proxies active, 2 quarantined]` | `>= 90% active` |
| **Total Execution Duration**| `[e.g., 1h 24m]` | - |
| **Average Request Latency** | `[e.g., 620ms]` | - |

---

## 2. Schema Quality & Coverage Audit

*Checked via `python scripts/miner_guard.py validate-records --data <file> --schema <schema>`*

| Field Name | Expected Type | Total Records | Null Count | Null % | Validation Failures |
|---|---|---|---|---|---|
| `item_id` | string (required) | `[5,000]` | `0` | `0.0%` | `0` |
| `title` | string (required) | `[5,000]` | `0` | `0.0%` | `0` |
| `price` | float (gt=0) | `[5,000]` | `8` | `0.16%` | `0` |
| `description`| string (optional) | `[5,000]` | `120` | `2.4%` | `0` |

* **Schema Verdict**: `[PASS - All required fields within null threshold (<5%)]`
* **PII Redaction Audit**: `[PASS - 0 unhashed emails/phone numbers detected]`

---

## 3. Selector Resilience & Drift Observations

* **API vs. HTML Breakdown**:
  * Records extracted via API: `[e.g., 4,200 (84%)]`
  * Records extracted via JSON-LD: `[e.g., 650 (13%)]`
  * Records extracted via DOM Selectors: `[e.g., 150 (3%)]`
* **Fallback Trigger Count**:
  * Secondary selector triggered: `[e.g., 42 times]`
  * DOM drift detected: `[None / Minor layout variation in category X]`

---

## 4. Output Artifacts & Data Provenance

* **Primary Dataset**: `[data/raw/catalog_batch_20260915.jsonl]`
* **Record Hash / Checksum**: `[SHA-256: 8f4e2...abc]`
* **Provenance Fields Embedded**:
  * `source_url`: Full origin URL
  * `extracted_at`: ISO-8601 UTC timestamp
  * `extractor_version`: Extractor Git commit / version ID

---

## 5. Downstream Handoff

* **Status**: Ready for downstream consumption.
* **Next Steps**:
  1. Hand off to `/exploratory-data-analysis`: Run EDA profiling to inspect feature distributions and outliers.
  2. Hand off to `/the-ml-engineer`: Ingest into feature store with crawl timestamps to preserve point-in-time accuracy.
