"""Reusable Python fixture for Axe-core accessibility auditing with Playwright.

Requires:
  pip install axe-core-python
"""

import pytest
from axe_core_python.sync_playwright import Axe

@pytest.fixture
def axe_scanner(page):
    """Provides a pre-configured Axe instance scoped to the active page."""
    axe = Axe()

    def _scan(include=None, exclude=None, tags=None):
        target_tags = tags or ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]
        results = axe.run(
            page,
            context={"include": include, "exclude": exclude} if include or exclude else None,
            options={"runOnly": target_tags},
        )
        return results

    return _scan
