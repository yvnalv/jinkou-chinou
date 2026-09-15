# Storage, Persistence & Data Sinks for Web Mining

The terminal objective of `/the-miner` is persisting validated, clean datasets into downstream storage backends. Scraped data is only valuable if it is reliably ingested without data corruption, truncation, duplicate entries, or pipeline deadlocks.

This reference specifies architecture patterns for persisting mined data across:
1. **Flat File Formats**: JSON Lines (`.jsonl`), CSV (`.csv`), Apache Parquet (`.parquet`).
2. **Relational Databases**: PostgreSQL, Microsoft SQL Server (`mssql`), SQLite.
3. **APIs & Streaming Ingestion**: REST endpoints, Webhooks, batch APIs.

---

## 1. Persistence Matrix & Target Selection

| Storage Target | Best For | Throughput | Deduplication / Upsert Strategy | Concurrency & Integrity |
|---|---|---|---|---|
| **JSON Lines (`.jsonl`)** | Raw dumps, streaming scraper output, nested semi-structured payloads | Ultra-High (append-only) | Post-process or hash set in memory | Zero lock contention; append line-by-line |
| **CSV (`.csv`)** | Tabular business analysis, spreadsheets, quick handoffs to Excel/EDA | High | In-memory key tracking or pandas dedup | Quoted strings; escape delimiters |
| **Apache Parquet (`.parquet`)** | Data lakes, big data pipelines, Polars/DuckDB/PySpark | Very High (compressed) | Write partition files; dedup at compaction | Strong typing; snappy/zstd compression |
| **PostgreSQL** | Production relational storage, JSONB queries, ACID pipelines | High (bulk copy) | `ON CONFLICT (id) DO UPDATE` (upsert) | Connection pooling (`asyncpg`), transaction batches |
| **SQL Server (`mssql`)** | Enterprise data warehouses, Microsoft ecosystems | High (bcp / MERGE) | `MERGE INTO ... USING` statements | Table locks on bulk insert; parameterized queries |
| **Downstream API / Webhook** | Event-driven ingest, third-party platforms, microservices | Moderate | Client-generated idempotency keys | Exponential backoff, batch POST payloads |

---

## 2. Flat File Sinks (.jsonl, .csv, .parquet)

### 2.1 JSON Lines (`.jsonl`) — The Standard Raw Output
* **Why JSONL**: Unlike standard `.json` arrays (which require parsing the entire multi-gigabyte array into memory), JSONL allows streaming append writes. If a crawler crashes mid-crawl, already written lines remain intact.
* **Streaming Writer**:
  ```python
  import json
  from pathlib import Path

  def append_record_jsonl(record: dict, output_path: Path) -> None:
      with output_path.open("a", encoding="utf-8") as fh:
          fh.write(json.dumps(record, ensure_ascii=False) + "\n")
  ```

### 2.2 CSV (`.csv`) — Formatting Rules
* Always use Python's built-in `csv.DictWriter` with `quoting=csv.QUOTE_MINIMAL` or `csv.QUOTE_ALL`.
* Flatten or serialize nested dictionaries/arrays into JSON strings before writing to prevent schema breakage.
* Ensure consistent header ordering across all records.

### 2.3 Apache Parquet (`.parquet`) — Columnar Storage
* For datasets exceeding 100,000 records, convert JSONL to Parquet using `pyarrow` or `polars`.
* Enables 75–90% disk space savings and instant querying in DuckDB, `/exploratory-data-analysis`, and `/the-ml-engineer`.

---

## 3. Relational Database Sinks (PostgreSQL & SQL Server)

### 3.1 Idempotency & Natural Primary Keys
Never perform naive raw `INSERT` queries on scrapers that re-run periodically. Always define an **Idempotency Key** or unique constraint based on natural keys:
* Primary Key candidates: `source_url`, `sku`, `product_id`, `listing_id`.
* Fallback synthetic key: `sha256(source_url + canonical_identifier)`.

### 3.2 PostgreSQL Ingestion Patterns
* **Upsert with `ON CONFLICT`**:
  ```sql
  INSERT INTO extracted_products (item_id, source_url, title, price, in_stock, raw_json, extracted_at)
  VALUES ($1, $2, $3, $4, $5, $6, $7)
  ON CONFLICT (item_id) DO UPDATE SET
      price = EXCLUDED.price,
      in_stock = EXCLUDED.in_stock,
      raw_json = EXCLUDED.raw_json,
      updated_at = NOW();
  ```
* **Bulk Streaming with `COPY FROM`**: For batches > 10,000 records, stream into a temporary staging table using PostgreSQL `COPY`, then run a single set-based `INSERT ... ON CONFLICT` into the target table.
* **Semi-Structured Payload Preservation**: Store full parsed payloads in a `JSONB` column (`raw_json`) alongside indexed tabular columns. This protects against data loss if newly added target attributes are not yet in the relational schema.

### 3.3 Microsoft SQL Server (`mssql`) Ingestion Patterns
* **Connecting via Python**: Use `pyodbc` or `pymssql` with connection pooling and ODBC Driver 18 for SQL Server:
  ```python
  import pyodbc

  conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=sql.example.com;DATABASE=DataWarehouse;UID=miner_app;PWD=SecretPass;TrustServerCertificate=yes;"
  ```
* **Upsert with `MERGE` Statement**:
  ```sql
  MERGE INTO CatalogProducts AS target
  USING (VALUES (?, ?, ?, ?, ?)) AS source (ItemId, SourceUrl, Title, Price, ExtractedAt)
  ON target.ItemId = source.ItemId
  WHEN MATCHED THEN
      UPDATE SET target.Price = source.Price,
                 target.ExtractedAt = source.ExtractedAt
  WHEN NOT MATCHED THEN
      INSERT (ItemId, SourceUrl, Title, Price, ExtractedAt)
      VALUES (source.ItemId, source.SourceUrl, source.Title, source.Price, source.ExtractedAt);
  ```
* **Bulk Loading (`fast_executemany`)**: When using `pyodbc`, always set `cursor.fast_executemany = True` before calling `executemany()` to batch network roundtrips into a single TDS protocol RPC call.

---

## 4. API & Webhook Sinks

When the pipeline pushes extracted data directly to downstream microservices, data ingest APIs, or message brokers (Kafka, RabbitMQ):

1. **Payload Batching**: Send records in chunks (e.g., 50–250 records per HTTP POST) to minimize network overhead and HTTP connection churn.
2. **Idempotency Headers**: Pass an `Idempotency-Key: <batch_hash>` header so retrying network timeouts does not create duplicate entries in the downstream consumer.
3. **Dead Letter Queue (DLQ)**: If the destination API returns HTTP 400 or 422 (malformed payload), save failed records to `data/dlq_failed_records.jsonl` rather than aborting the entire mining run.

---

## 5. Storage Integrity Checklist

Before marking an extraction job complete, verify:

- [ ] Records are written in batches (e.g., 500 records per batch) with transactional integrity.
- [ ] Primary keys or unique constraints prevent duplicate rows on re-runs.
- [ ] Raw extracted JSON is retained in a `raw_payload` / `raw_json` column or alongside `.jsonl` archives.
- [ ] Timestamps are stored in UTC (`YYYY-MM-DDTHH:MM:SSZ`).
- [ ] Database connections use connection pooling and close gracefully on crawler exit.
- [ ] Storage write failures trigger retries with exponential backoff before routing to DLQ.
