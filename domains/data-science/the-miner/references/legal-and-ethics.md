# Legal and Ethical Framework for Data Collection & Web Mining

Automated data collection and web mining exist at the intersection of technical capability, terms of service, intellectual property law, and privacy regulations. As an expert data miner, adherence to legal boundaries and ethical engineering ensures sustainability, prevents civil or criminal liability, and protects system availability.

---

## 1. Legal Foundations & Precedents

### 1.1 Computer Fraud and Abuse Act (CFAA) & Access Authorization
* **Publicly Accessible Data**: Under the landmark US 9th Circuit ruling in *hiQ Labs v. LinkedIn Corp.* (2022) and the Supreme Court precedent in *Van Buren v. United States* (2021), accessing publicly available web data without authentication does not constitute "access without authorization" or "exceeding authorized access" under the CFAA (18 U.S.C. § 1030).
* **Authenticated Gates & Revoked Access**:
  * If a website requires user credentials, session cookies, or account sign-in to view data, access is governed strictly by the user agreement.
  * Explicit Cease & Desist (C&D) notices or formal revocation of access may eliminate claims of authorized access.
  * **Rule**: Never attempt to bypass authentication walls, paywalls, or cryptographic access controls.

### 1.2 Terms of Service (ToS) & Breach of Contract
* **Browsewrap vs. Clickwrap Agreements**:
  * *Browsewrap* (ToS links tucked in page footers without explicit user assent) is frequently scrutinized and holds weaker enforceability against automated agents unless actual notice is established.
  * *Clickwrap* (explicit "I Agree" during account registration) creates a binding bilateral contract.
* **Prudent Engineering**:
  * Even on public web properties, design collection pipelines to minimize system burden and respect reasonable access terms.
  * When scraping under authenticated accounts, document the contractual risk profile in `EXTRACTION_SPEC.md`.

### 1.3 Intellectual Property & Copyright
* **Facts vs. Creative Expression**:
  * Raw facts, catalog numbers, tabular statistics, public pricing, and directory listings are not copyrightable under the *Feist Publications, Inc. v. Rural Telephone Service Co.* doctrine (the "sweat of the brow" doctrine is rejected; only original creative arrangement or expression is protected).
  * Creative expression (long-form editorial text, original reviews, proprietary photographs, video, and audio) retains copyright protection.
* **Fair Use & Transformative Processing**:
  * Extracting factual data elements for statistical aggregation, training classification models, or index creation is commonly defensible under Fair Use (US 17 U.S.C. § 107) or text and data mining (TDM) exemptions (EU Directive on Copyright in the Digital Single Market, Articles 3 & 4).
  * Direct wholesale republication or competitive redistribution of proprietary creative databases is prohibited.

---

## 2. Privacy & Data Protection (GDPR, CCPA, CPRA)

### 2.1 Personal Data & PII at Ingestion
* **Definition**: Any information relating to an identified or identifiable natural person (names, email addresses, phone numbers, personal social media handles, home addresses, IP addresses).
* **Principle of Purpose Limitation & Data Minimization**:
  * Do not scrape personal data unless explicitly in scope and backed by a lawful basis (e.g., legitimate interests, consent).
  * Apply field-level redaction or hashing at the extraction boundary. If an email, phone number, or user address is extracted inadvertently, filter or mask it before serializing to storage.
* **Prohibited Mining**:
  * Scraping personal profiles from social networks to build unregulated biometric databases or non-consensual surveillance registries is strictly prohibited.

---

## 3. Robots Exclusion Standard (`robots.txt`)

### 3.1 Interpretation & Scope
* The `robots.txt` protocol (RFC 9309) is the primary voluntary standard for webmasters to signal crawl preferences.
* Inspect `https://<domain>/robots.txt` before deploying collectors.
* Audit rules for the targeted User-Agent (and fallback `User-Agent: *`):
  * `Disallow: /` — Entire domain is off-limits.
  * `Disallow: /private-api/` — Specific paths to avoid.
  * `Crawl-delay: <seconds>` — Minimum delay between consecutive requests from the same crawler.
  * `Sitemap: <url>` — Preferred method for finding discoverable resources without spidering.

### 3.2 Decision Matrix for Disallow Directives
1. If `robots.txt` disallows the target endpoint:
   - Check if an official public API, RSS feed, or open data dump exists.
   - If no alternative exists, assess if the data is purely public, and if proceeding is defensible under fair use/research. Log the `robots.txt` exclusion explicitly as an acknowledged policy decision in `EXTRACTION_SPEC.md`.
   - Never force crawl paths containing administrative portals, user session endpoints, or staging environments.

---

## 4. Rate Limiting, Infrastructure Courtesy & Anti-DDoS

### 4.1 Server Impact & Capacity Preservation
* High-frequency scraping can degrade target service for human users or incur heavy cloud egress costs for the publisher.
* **Default Concurrency & Delays**:
  * Set max concurrent workers per target host (recommended: 1 to 3 concurrent connections for medium sites; never flood a single origin with 50+ concurrent workers).
  * Implement randomized delay (Gaussian jitter) between successive requests (e.g., base delay $1.5\text{s} \pm 0.5\text{s}$).
* **HTTP 429 & 503 Handling**:
  * `429 Too Many Requests`: Back off immediately using exponential backoff with jitter. Honor `Retry-After` response headers if present.
  * `503 Service Unavailable`: Target server is overloaded; pause all threads targeting that origin for a cooldown period (minimum 60 seconds).

### 4.2 Transparent Identification
* Where organizational policy permits, identify the crawler via the `User-Agent` string with a contact email or project URL:
  ```http
  User-Agent: ResearchScraper/1.0 (+https://example.com/bot; bot@example.com)
  ```
* When anonymity/stealth is required to avoid commercial competitive blocking on public catalog data, configure headers that resemble standard desktop browsers without impersonating unauthorized internal credentials.

---

## 5. Ethical Compliance Checklist

Every extraction job managed by `/the-miner` must pass this checklist:

- [ ] Data is publicly accessible without bypassing login or paywall controls.
- [ ] `robots.txt` has been audited and recorded via `miner_guard.py check-robots`.
- [ ] Concurrency and jitter rules are configured to prevent server degradation.
- [ ] PII redaction rules are active at the extractor transform boundary.
- [ ] Data provenance metadata (source URL, crawl timestamp, content hash) is embedded.
- [ ] Target host errors (429/503) trigger immediate throttling and cool-down.
- [ ] Commercial/licensing implications of the collected dataset have been documented.
