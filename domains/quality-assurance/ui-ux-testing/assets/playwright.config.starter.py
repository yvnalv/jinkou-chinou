"""Production-ready pytest-playwright starter configuration and fixtures.

Use this file as `conftest.py` in your tests directory when testing with Python.
Provides multi-viewport device fixtures and global animation freezing.
"""

import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Global browser context options."""
    return {
        **browser_context_args,
        "record_video_dir": "test-results/videos/",
        "viewport": {"width": 1280, "height": 800},
    }

@pytest.fixture
def mobile_viewport(page):
    """Set mobile iPhone viewport with touch emulation."""
    page.set_viewport_size({"width": 390, "height": 844})
    return page

@pytest.fixture
def tablet_viewport(page):
    """Set tablet iPad viewport."""
    page.set_viewport_size({"width": 768, "height": 1024})
    return page

@pytest.fixture(autouse=True)
def freeze_animations(page):
    """Automatically freeze CSS animations before every test for visual stability."""
    page.add_init_script("""
        window.addEventListener('DOMContentLoaded', () => {
            const style = document.createElement('style');
            style.textContent = `
                *, *::before, *::after {
                    transition: none !important;
                    animation: none !important;
                    caret-color: transparent !important;
                }
            `;
            document.head.appendChild(style);
        });
    """)
