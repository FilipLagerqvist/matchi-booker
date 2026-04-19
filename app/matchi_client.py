from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from dataclasses import dataclass
import time


@dataclass
class MatchiSession:
    playwright: any
    browser: Browser
    context: BrowserContext
    page: Page

    def close(self) -> None:
        self.context.close()
        self.browser.close()
        self.playwright.stop()


class MatchiClient:
    def __init__(self, email: str, password: str, headless: bool = False):
        self.email = email
        self.password = password
        self.headless = headless

    def start(self) -> MatchiSession:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=self.headless)
        context = browser.new_context()
        page = context.new_page()
        
        return MatchiSession(playwright, browser, context, page)
    
    def login(self, session: MatchiSession) -> None:
        page = session.page
        page.goto("https://www.matchi.se/login", wait_until="domcontentloaded")

        # May need to adjust selectors
        page.locator('input[type="email"]').fill(self.email)
        page.locator('input[type="password"]').fill(self.password)
        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")
        time.sleep(2)

    def open_facility(self, session: MatchiSession, facility_url: str) -> None:
        session.page.goto(facility_url, wait_until="domcontentloaded")
        session.page.wait_for_load_state("networkidle")