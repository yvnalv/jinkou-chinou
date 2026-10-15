# Selenium WebDriver Fallback & Integration Guide

While Playwright is the primary standard for modern UI/UX test automation, Selenium WebDriver remains prevalent in legacy or enterprise repositories (particularly Java, C#, or Python ecosystems). This reference outlines how to execute UI/UX testing principles within a Selenium codebase.

---

## 1. Emulating Auto-Waiting via Explicit Waits

Selenium lacks Playwright's built-in auto-waiting engine. **Never use `time.sleep()` in Selenium tests.** Always wrap interactions in explicit `WebDriverWait` constructs.

### Python Example with Explicit Wait Helper
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_when_ready(driver, by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element

def get_text_when_visible(driver, by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )
    return element.text
```

---

## 2. Automated Accessibility Testing with Selenium

Integrate Deque's `axe-core` via `axe-selenium-python`:

### Installation
```bash
pip install axe-selenium-python
```

### Test Case with Axe Injection
```python
import pytest
from selenium import webdriver
from axe_selenium_python import Axe

def test_homepage_accessibility():
    driver = webdriver.Chrome()
    driver.set_window_size(1280, 800)
    driver.get("https://example.com")

    axe = Axe(driver)
    # Inject axe-core into page
    axe.inject()
    # Run audit with WCAG 2.1 AA rules
    results = axe.run(options={"runOnly": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]})

    driver.quit()

    violations = results.get("violations", [])
    assert len(violations) == 0, f"Found {len(violations)} accessibility violations: {violations}"
```

---

## 3. Visual Regression in Selenium (Using Pillow)

Because Selenium has no native `toHaveScreenshot()` assertion, capture screenshots and calculate pixel difference using Python's `PIL` (Pillow):

```python
import io
from PIL import Image, ImageChops

def compare_screenshots(current_png_bytes, baseline_path, max_diff_percent=1.0):
    current_img = Image.open(io.BytesIO(current_png_bytes)).convert("RGB")
    baseline_img = Image.open(baseline_path).convert("RGB")

    diff = ImageChops.difference(current_img, baseline_img)
    diff_bbox = diff.getbbox()

    if not diff_bbox:
        return True, 0.0  # Identical

    # Calculate percentage of non-zero pixels
    stat = diff.histogram()
    # If diff exceeds tolerance, report failure
    total_pixels = current_img.size[0] * current_img.size[1]
    # Evaluate diff tolerance
    # ...
```

---

## 4. When to Propose Migrating from Selenium to Playwright

If a team experiences frequent flakiness with Selenium, recommend migrating:
* **Flakiness**: Playwright automatically handles animations, visibility checks, and network events.
* **Speed**: Playwright executes directly over WebSocket CDP, avoiding WebDriver HTTP hop overhead.
* **All-in-One**: Playwright provides native visual regression, mobile emulation, and tracing out of the box without third-party plugins.
