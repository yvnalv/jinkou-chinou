# Anti-Blocking, Stealth & Proxy Management

Modern websites protect their public catalog and content using sophisticated Web Application Firewalls (WAFs) and bot-management platforms (Cloudflare, Akamai, DataDome, PerimeterX/HUMAN, Kasada, AWS WAF).

Naive scrapers using standard libraries (`urllib`, Python `requests`) are blocked immediately because their network and protocol signatures do not match legitimate user agents. Expert data mining requires an understanding of fingerprinting layers, proxy pool orchestration, and browser behavior emulation.

---

## 1. The Multi-Layer Bot Detection Stack

Bot management solutions evaluate incoming requests across four distinct OSI and application layers:

```text
Layer 1: IP Reputation & ASN        (Datacenter vs Residential vs Mobile IP, Geolocation, AbuseDB)
Layer 2: TLS Fingerprint (JA3/JA4)  (Cipher suites, extensions, elliptic curves, ALPN)
Layer 3: HTTP/2 Protocol Frames     (SETTINGS parameters, pseudo-header ordering, window size)
Layer 4: Browser Execution Context  (navigator.webdriver, Canvas/WebGL/Audio hash, mouse/scroll cadence)
```

If a client sends a Chrome 130 `User-Agent` string over a raw Python OpenSSL socket with a Linux TLS fingerprint and standard HTTP/1.1 headers, the anomaly is flagged instantly and blocked with HTTP 403 or a CAPTCHA challenge.

---

## 2. TLS & HTTP/2 Fingerprint Alignment

### 2.1 TLS Fingerprinting (JA3 / JA4)
* When initiating a TLS handshake, the client sends a `Client Hello` packet containing:
  * Supported TLS version (e.g., TLS 1.3)
  * Cipher suites in priority order
  * Supported extensions (Server Name Indication, supported groups, signature algorithms)
  * Elliptic curves and point formats
* Anti-bot systems hash these attributes into a **JA3** or **JA4** signature and cross-reference it with known browser databases.
* Standard Python `requests` or `aiohttp` rely on Python's bundled OpenSSL, producing a fingerprint identical to generic automated scripts, regardless of what `User-Agent` header is passed.

### 2.2 HTTP/2 Protocol Fingerprinting
* In HTTP/2, browsers negotiate specific connection parameters:
  * Initial `SETTINGS` frames (`HEADER_TABLE_SIZE`, `ENABLE_PUSH`, `MAX_CONCURRENT_STREAMS`, `INITIAL_WINDOW_SIZE`)
  * Pseudo-header order: Real Chrome strictly sends `:method`, `:authority`, `:scheme`, `:path`. Sending them out of order or omitting pseudo-headers flags the request.
  * `WINDOW_UPDATE` frames and priority tree definitions.

### 2.3 Recommended Client Engines
To achieve authentic network signatures without the heavyweight overhead of a full browser:
* **`curl_cffi`**: Python binding for `curl-impersonate`. Capable of natively mimicking the exact TLS, JA4, and HTTP/2 signatures of modern Chrome, Edge, Safari, and Firefox.
* **`tls-client`**: Lightweight HTTP library built on Go's `tls-client` library, supporting pre-configured browser profiles.

*Example with `curl_cffi`:*
```python
from curl_cffi import requests

# Impersonates modern Chrome TLS handshake and HTTP/2 frames
response = requests.get(
    "https://target-catalog.example.com/items",
    impersonate="chrome124",
    headers={"Accept-Language": "en-US,en;q=0.9"},
)
print(response.status_code, len(response.content))
```

---

## 3. Proxy Architectures & IP Rotation

An IP address is the foundational identity in rate-limiting algorithms. Distributing requests across trusted IP pools prevents rate-limit exhaustion and IP-level blacklisting.

### 3.1 Proxy Types Comparison

| Proxy Class | Origin | Cost | Detection Risk | Ideal Use Case |
|---|---|---|---|---|
| **Datacenter** | Cloud hosting (AWS, DigitalOcean, Hetzner) | Low ($) | High (ASN flagged as server hosting) | High-volume public APIs, sites without WAFs, initial sitemap discovery |
| **Residential** | Consumer ISP connections (Comcast, AT&T, residential fiber) | Medium–High ($$$) | Low (indistinguishable from home users) | Anti-bot protected sites (Cloudflare, Akamai), localized pricing |
| **Mobile (4G/5G)** | Cellular carrier networks (CGNAT pools) | High ($$$$) | Near Zero (hundreds of real users share the same cellular IP) | Aggressive security targets (DataDome, Kasada), login/session operations |

### 3.2 Rotation Strategies: Per-Request vs. Sticky Sessions
1. **Per-Request Rotation**:
   * Every HTTP request passes through a different proxy IP.
   * *Best for*: Stateless scraping (single product pages, sitemaps, independent detail pages).
   * *Risk*: High churn rate; breaks sites requiring cookies, session state, or shopping carts.
2. **Sticky Sessions (Session Persistence)**:
   * A single proxy IP is bound to a crawler thread for a specific duration (e.g., 5 to 30 minutes) or until a session ID changes.
   * *Best for*: Multi-step navigation (search → filter → paginate page 1 to 5 → detail page), authenticated sessions.
   * Configure proxy gateway parameters (e.g., `http://user-session_12345:pass@proxy.example.com:8080`).

### 3.3 Proxy Pool Hygiene & Fault Tolerance
* **Dead Proxy Eviction**: Any proxy returning connection timeouts, connection resets, or HTTP 407 (Proxy Auth Required) 3 consecutive times should be quarantined for 15 minutes.
* **Geotargeting**: Match proxy exit country/region with the target website's expected audience (e.g., scrape a UK retailer using UK residential IPs).
* **Circuit Breaker**: If >20% of proxies in a pool receive HTTP 403 or 429 within a 5-minute window, pause crawler operations and alert the operator.

---

## 4. Headless Browser Stealth & Automation

When JavaScript rendering, canvas challenges, or client-side hydration are unavoidable, use headless browser automation (Playwright) enhanced with stealth overrides.

### 4.1 Fingerprint Masking
Standard headless Chrome leaks dozens of automation flags that bot detectors inspect via JavaScript:

```javascript
// Leaks present in default headless browsers:
navigator.webdriver === true              // Must be deleted or set to false
navigator.plugins.length === 0            // Must emulate realistic plugin array
window.chrome === undefined               // Must mock Chrome runtime
navigator.languages === ['en-US']         // Must align with Accept-Language
WebGLRenderer === "Google SwiftShader"    // Software rendering; must spoof GPU (e.g., ANGLE Intel Iris)
```

*Implementation with Playwright & Stealth:*
* Use `playwright-stealth` or configure modern `patchright` / `undetected-playwright`.
* Run in realistic viewport sizes (e.g., `1920x1080` or `1440x900`), avoiding default `800x600`.
* Enable standard font packs and hardware acceleration where possible.

### 4.2 Human Behavioral Emulation
Automated scripts interact with zero delay and unnatural trajectories. Sophisticated telemetry monitors user input events:
* **Mouse Movement**: Never use instant pointer jumps. Employ cubic Bézier curves with randomized control points and variable speeds.
* **Scroll Dynamics**: Scroll in stepped bursts with realistic decelerations (momentum scrolling) rather than calling `window.scrollTo(0, 10000)`.
* **Typing Cadence**: For search bars and form inputs, inject per-keystroke delays ($70\text{ms} - 180\text{ms}$) with occasional micro-pauses.

---

## 5. Header Hygiene & Client Hints

Headers must represent a consistent, cohesive browser persona.

### 5.1 The Modern Header Set (Chromium Baseline)
```http
Host: target.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br, zstd
Sec-Ch-Ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
```

### 5.2 Header Traps to Avoid
* Never send conflicting headers (e.g., `Sec-Ch-Ua-Platform: "Windows"` with a macOS `User-Agent`).
* Never omit modern `Sec-Fetch-*` headers when targeting modern web properties; their absence immediately flags a legacy HTTP client.
* Maintain proper header casing if using raw sockets or custom proxies.

---

## 6. Ban Detection & Recovery Protocols

| Signal | Meaning | Immediate Action |
|---|---|---|
| **HTTP 403 Forbidden** | WAF block or IP blacklist triggered | Switch proxy IP; inspect TLS fingerprint; switch to `curl_cffi` or stealth browser. |
| **HTTP 429 Too Many Requests** | Rate limit threshold exceeded | Back off immediately (exponential backoff); rotate proxy; increase base request jitter ($3\text{s} - 8\text{s}$). |
| **HTTP 503 + Cloudflare Challenge** | JavaScript / Turnstile challenge page | Route through headless stealth browser with residential IP to solve challenge; extract cookies and reuse in `curl_cffi` session. |
| **Blank HTML or Honeypot Content** | Silent shadowban or DOM spoofing | Check response body size against baseline; verify expected schema fields; discard record. |
