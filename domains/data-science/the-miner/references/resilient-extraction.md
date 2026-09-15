# Resilient Extraction for Dynamic & Mutating Web Structures

A primary failure mode of production web scrapers is fragility against HTML layout shifts. Modern web platforms frequently change DOM structures through weekly frontend deployments, A/B tests, framework migrations (e.g., React to Next.js), and CSS-in-JS tooling that generates randomized class names (e.g., `.style__1a8z_9` or Tailwind utility classes).

An expert data miner does not write brittle CSS selectors tied to temporary visual classes. Instead, extraction follows a **Resilience Ladder**, defensive schema validation, and automated DOM drift detection.

---

## 1. The Extraction Resilience Ladder

Always attempt extraction at the lowest possible rung of the ladder before falling back to more fragile methods:

```text
Rung 1: Network Inspection & Internal APIs      (Most resilient, structured JSON, highest throughput)
Rung 2: Embedded Hydration Data & JSON-LD       (Stable schema.org data, __NEXT_DATA__, state blobs)
Rung 3: Semantic & Accessibility Attributes     (data-testid, ARIA roles, itemprop, <time>, <article>)
Rung 4: Multi-Candidate Fallback Selector Chains(Prioritized CSS/XPath cascades with text anchoring)
Rung 5: Semantic Layout / LLM-Guided Fallback   (Visual or structural LLM extraction for high-drift pages)
```

---

## 2. Rung 1: Network Inspection & API Reverse Engineering

Modern Single-Page Applications (SPAs) and mobile web clients fetch data from backend JSON/GraphQL endpoints. Finding and querying these endpoints directly bypasses HTML rendering and DOM shifts entirely.

### 2.1 Discovery Technique
1. Open DevTools (`F12`) → Network tab. Filter by `Fetch/XHR`.
2. Reload the page, trigger search, scroll for infinite pagination, or click category filters.
3. Look for requests returning JSON payloads with MIME type `application/json`.
4. Inspect the Request Headers:
   - Identify required authentication tokens (e.g., `Authorization: Bearer ...`, `X-API-Key`, or session cookies).
   - Check if an API key is static/public in client-side bundles (`main.js` or `app.js`).
5. Replicate the request directly via `curl_cffi` or standard HTTP client.

*Advantages*: 10x–50x faster execution, zero headless browser RAM overhead, standardized JSON structures that rarely change when frontend designs change.

---

## 3. Rung 2: Embedded Metadata & Hydration State

If no direct API exists or requests are signed cryptographically, inspect the raw HTML document for pre-rendered server state and structured metadata before writing DOM queries.

### 3.1 JSON-LD (Schema.org)
Webmasters embed JSON-LD metadata for search engine indexing (SEO). This data follows standardized schema.org specifications (`Product`, `Article`, `Event`, `JobPosting`, `LocalBusiness`) and persists across major frontend redesigns.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Industrial Sensor Model X",
  "sku": "IS-9000",
  "offers": {
    "@type": "Offer",
    "price": "249.99",
    "priceCurrency": "USD"
  }
}
</script>
```

*Extraction Rule*: Always check for `//script[@type="application/ld+json"]` before parsing visible HTML markup.

### 3.2 Framework Hydration Payloads
Modern SSR frameworks serialize initial backend state directly into HTML tags:
* **Next.js**: `<script id="__NEXT_DATA__" type="application/json">` contains the exact page properties passed from `getServerSideProps` or `getStaticProps`.
* **Nuxt.js**: `window.__NUXT__` JavaScript variable.
* **Remix / Vite SSR**: `<script>window.__remixContext = ...</script>`.

Parsing these JSON script tags provides clean, strongly typed data dictionaries with zero DOM parsing.

---

## 4. Rung 3 & 4: Robust DOM Selectors & Fallback Chains

When extracting from visible HTML, avoid visual styling classes (e.g., `.flex.items-center.text-red-500` or `.css-19v8z2`). These break during design updates.

### 4.1 Hierarchy of Selector Stability

| Priority | Selector Pattern | Example | Why It Resists Drift |
|---|---|---|---|
| **1 (Best)** | Dedicated Test / Data Attributes | `[data-testid="product-price"]` | Developers explicitly preserve these for automated tests. |
| **2** | Microdata / Schema Attributes | `[itemprop="price"]` | Maintained for search engines; rarely removed. |
| **3** | Accessibility / ARIA Roles | `article[role="article"]`, `[aria-label="Add to cart"]` | Regulated for accessibility compliance. |
| **4** | Semantic HTML5 Elements | `<article>`, `<header>`, `<main>`, `<time datetime="...">` | Core HTML semantics remain stable across re-skins. |
| **5** | Contextual XPath Anchors | `//h2[contains(text(), "Specs")]/following-sibling::table` | Anchored on business concepts rather than class names. |
| **6 (Avoid)** | Hash-generated CSS classes | `.styled__sc-14a9...`, `.css-xyz` | Regenerated on every application build. |

### 4.2 Multi-Candidate Fallback Chains
Define extraction rules as ordered cascades. If the primary selector yields null or fails type coercion, the extractor tries secondary and tertiary candidates:

```python
SELECTOR_CASCADES = {
    "price": [
        {"type": "json_ld", "path": "offers.price"},
        {"type": "css", "query": "[data-testid='price']::text"},
        {"type": "css", "query": "span[itemprop='price']::text"},
        {"type": "xpath", "query": "//span[contains(@class, 'price')]/text()"},
    ],
    "title": [
        {"type": "json_ld", "path": "name"},
        {"type": "css", "query": "h1[data-testid='product-title']::text"},
        {"type": "css", "query": "h1.product-title::text"},
        {"type": "xpath", "query": "//main//h1/text()"},
    ]
}
```

---

## 5. Defensive Schema Validation with Pydantic

Never pass unvalidated raw strings from HTML into downstream datasets or databases. Define strict Pydantic models at the extraction boundary to enforce data types, presence of required fields, and boundary constraints.

```python
from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
from typing import Optional

class ExtractedProduct(BaseModel):
    source_url: HttpUrl
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    sku: str = Field(min_length=3, max_length=64)
    title: str = Field(min_length=1)
    price: float = Field(gt=0.0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    in_stock: bool
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)

    @field_validator("price", mode="before")
    @classmethod
    def clean_price(cls, v):
        if isinstance(v, str):
            # Strip currency symbols and whitespace: "$249.99" -> 249.99
            cleaned = re.sub(r"[^\d.]", "", v)
            return float(cleaned) if cleaned else None
        return v
```

### 5.1 The Null Threshold Circuit Breaker
* If an extraction run reports that a required field (`title`, `price`) is null in **>5% of scraped records**, the pipeline must immediately trigger an alert and pause batch commits.
* A spike in null rates indicates that the target website deployed a structural change that bypassed primary selectors.

---

## 6. DOM Drift Detection & Recovery

Use `scripts/miner_guard.py diff-dom` to compare historical baseline HTML snapshots against newly captured pages:

1. **Snapshot Archiving**: Periodically save representative raw HTML snapshots of key target pages (e.g., `tests/fixtures/product_baseline.html`).
2. **Structural Drift Audit**:
   ```bash
   python scripts/miner_guard.py diff-dom \
     --baseline tests/fixtures/baseline.html \
     --current tests/fixtures/current_sample.html \
     --schema config/product_schema.json
   ```
3. **Drift Triage**:
   - If attributes moved from visible text to JSON-LD, shift to Rung 2.
   - If class names were obfuscated, switch to `data-testid` or XPath sibling navigation.
   - Update `SELECTOR_CASCADES` and record the change in the job changelog.
