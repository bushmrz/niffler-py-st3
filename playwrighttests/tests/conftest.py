import pytest
from playwright.sync_api import sync_playwright, Page

BASE_URL = "http://frontend.niffler.dc"

@pytest.fixture()
def playwright_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        browser.close()

@pytest.fixture
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()