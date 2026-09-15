# Extraction Specification: [Target Name / Domain]

*Date: [YYYY-MM-DD] | Status: [Draft | Approved | Active] | Author: [/the-miner]*

---

## 1. Executive Summary & Objective

* **Target System**: `[e.g., Target Marketplace Catalog / Public Job Board]`
* **Origin URL(s)**: `[https://example.com/catalog]`
* **Business Objective**: `[e.g., Aggregate weekly pricing data for market research]`
* **Downstream Consumers**: `[e.g., /exploratory-data-analysis, /the-ml-engineer, /the-ai-engineer]`

---

## 2. Legal, Ethical & Compliance Scope

* **Public Accessibility**: `[Yes - data is public / No login required]`
* **Robots.txt Assessment**:
  * Status: `[Allowed / Disallowed path / Crawl-delay specified]`
  * Directives audited: `[e.g., Disallow: /admin, Crawl-delay: 2]`
  * `miner_guard.py check-robots` verdict: `[PASS / EXCLUSION NOTED]`
* **Terms of Service (ToS) Review**: `[Summary of relevant browsewrap/clickwrap clauses]`
* **Personal Identifiable Information (PII)**:
  * Present in raw payload? `[Yes / No]`
  * Redaction / Masking Strategy: `[e.g., Hash email addresses, drop phone numbers at extractor]`
* **Copyright & Transformative Use**: `[Factual data only; no creative media redistributions]`

---

## 3. Network, Stealth & Proxy Architecture

* **Engine Choice**: `[curl_cffi (Chrome impersonation) / Playwright Stealth / Requests]`
* **TLS & Protocol Profile**: `[e.g., Chrome 124 JA4 fingerprint + HTTP/2]`
* **Proxy Configuration**:
  * Proxy Class: `[Datacenter / Residential / Mobile]`
  * Rotation Pattern: `[Per-request / Sticky sessions (5 min duration)]`
  * Geotargeting: `[e.g., US / UK / Global]`
* **Rate Limits & Courtesy Budget**:
  * Max Concurrent Workers: `[e.g., 2 workers]`
  * Request Delay & Jitter: `[e.g., 2.0s base delay +/- 0.8s Gaussian jitter]`
  * Cooldown on 429/503: `[Exponential backoff: 5s, 15s, 45s, then 5 min quarantine]`

---

## 4. Extraction Strategy & Resilience Ladder

* **Target Endpoints / Sources**:
  * Primary: `[e.g., Internal JSON API: /api/v2/products?page=N]`
  * Secondary (HTML Fallback): `[e.g., SSR HTML with embedded JSON-LD]`
* **Selector Cascades**:
  | Field | Primary Selector | Secondary Fallback | Tertiary Fallback |
  |---|---|---|---|
  | `item_id` | JSON payload `.id` | `[data-testid="sku"]` | `meta[itemprop="sku"]` |
  | `title` | JSON payload `.name` | `h1[itemprop="name"]` | `h1.product-title` |
  | `price` | JSON payload `.price` | `span[itemprop="price"]` | `[data-testid="price"]` |
  | `category` | JSON payload `.category` | `ol.breadcrumbs li:last-child` | `nav.breadcrumb a` |

---

## 5. Target Schema & Validation Rules

* **Output Format**: `[JSON Lines (.jsonl) / Parquet / CSV]`
* **Pydantic Model Schema**:
  ```python
  # Target model specification
  ```
* **Critical Null Threshold**: `[Pause pipeline if required field null rate exceeds 5%]`

---

## 6. Handoff & Downstream Pipeline

* **Data Destination**: `[e.g., data/raw/products_2026-09.jsonl]`
* **Downstream Skill Trigger**:
  * `[ ]` `/exploratory-data-analysis` — Profile distributions, nulls, cardinality
  * `[ ]` `/the-ml-engineer` — Ingest as point-in-time training features
  * `[ ]` `/the-ai-engineer` — Ingest into vector store / RAG knowledge base
