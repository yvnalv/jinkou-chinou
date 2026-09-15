# the-miner

Data acquisition, web mining, extraction, and persistence expert persona for data science: design, build, audit, and maintain resilient data collection pipelines across modern web architectures, storing results in flat files (.csv, .jsonl, .parquet), relational databases (PostgreSQL, SQL Server, SQLite), and APIs. Combines stealth engineering (TLS/JA4 fingerprinting, residential proxy rotation, browser fingerprint masking) with structural resilience (internal API discovery, JSON-LD, multi-candidate fallback selectors, Pydantic schema validation), idempotent persistence (upserts, natural keys), and ethical/legal compliance (robots.txt auditing, rate limiting with jitter, PII redaction under GDPR/CCPA).

## When to use

Invoke `/the-miner` (or ask for data collection, web scraping, data mining, or storing web data into databases/files) when:
* Building automated data collectors for dynamic websites, SPAs, or JavaScript-heavy pages.
* Persisting mined data into storage: CSV spreadsheets, JSON Lines streaming files, Parquet data lakes, or relational databases (PostgreSQL with `ON CONFLICT`, Microsoft SQL Server with `MERGE`, SQLite).
* Bypassing anti-bot defenses (Cloudflare, Akamai, DataDome) on public catalogs using ethical proxy rotation and TLS impersonation.
* Scrapers broke due to website redesigns, dynamic class names, or DOM structural drift.
* Establishing legal and ethical boundaries: auditing `robots.txt`, setting courtesy rate budgets, and redacting PII before dataset storage.
* Extracting and structuring web data to feed downstream data science (`/exploratory-data-analysis`), ML modeling (`/the-ml-engineer`), or RAG pipelines (`/the-ai-engineer`).

Do not use for: exploratory data analysis on existing datasets (use `/exploratory-data-analysis`), training predictive ML models (use `/the-ml-engineer`), or building general software backend architecture (use `/the-architect`).

## Structure

```text
the-miner/
├── SKILL.md                          # Persona instructions, modes, gates, and rules
├── README.md                         # Human-facing overview, usage guide, changelog
├── config/
│   └── skill.yaml                    # Machine-readable manifest and domain policies
├── references/
│   ├── legal-and-ethics.md           # robots.txt, CFAA, GDPR/CCPA, ToS, rate limits
│   ├── anti-blocking-and-proxies.md  # TLS/JA4 fingerprinting, proxy rotation, browser stealth
│   ├── resilient-extraction.md       # API discovery, JSON-LD, fallback ladders, drift detection
│   ├── storage-and-persistence.md    # Multi-sink persistence (.csv, .parquet, PostgreSQL, SQL Server, APIs)
│   ├── EXTRACTION_SPEC.template.md   # Planning template for scraping jobs
│   └── MINING_REPORT.template.md     # Output provenance and data quality report
├── scripts/
│   └── miner_guard.py                # Stdlib CLI: robots.txt, validate-records, diff-dom, export
└── evals/
    └── evals.json                    # Trigger and behavior test cases
```

## Changelog

### 0.2.0 — 2026-09-15

* Added multi-sink storage and persistence: flat files (.csv, .jsonl, .parquet), relational databases (PostgreSQL, SQL Server, SQLite), and API webhooks.
* Added `references/storage-and-persistence.md` covering idempotent upserts (`ON CONFLICT`, `MERGE`), connection pooling, batching, and dead-letter queues.
* Added `export` command to `scripts/miner_guard.py` for exporting JSONL records into CSV, JSON, SQL DDL/INSERTs (postgres/sqlserver/sqlite), or SQLite databases.
* Added Storage Integrity Gate to `SKILL.md` and updated `config/skill.yaml`.

### 0.1.0 — 2026-09-15

* Initial release of `/the-miner` as the core data collection and web mining persona in `data-science`.
* Five operational modes: Reconnaissance (A), Pipeline Build (B), Drift Repair (C), Compliance Review (D), Quick Extraction (E).
* Reference guides for legal/ethics, anti-blocking/proxies, and resilient extraction.
* Built-in `miner_guard.py` CLI supporting `check-robots`, `validate-records`, and `diff-dom`.
* Integration and handoff pathways to `/exploratory-data-analysis`, `/the-ml-engineer`, and `/the-ai-engineer`.
