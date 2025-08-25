import time

from playwright.sync_api import sync_playwright
from loguru import logger

# from modules.scripts import GET_AREAS


GET_AREAS = """
const regions = [];

window.document.querySelectorAll('li[data-test="filter-region-item"]').forEach(li => {
    const btn = li.querySelector('button');
    const alias = btn?.getAttribute('data-alias');
    const label = li.querySelector('span[data-test="filter-item-label"]')?.textContent.trim();

    if (label) {
        regions.push({ alias, label });
    }
});
regions;
"""


class ChromeBrowser:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        )
        self.page = self.browser.new_page()
        self.page.set_default_timeout(60000)
        logger.info("Browser opened")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser closed")

    def start_parsing(self, url: str):
        self.page.goto(url=url)
        # more_btn = self.page.locator(selector=".FilterGroup__toggle")
        # self.page.evaluate(
        #     expression="window.document.querySelector('.FilterGroup__toggle').click()"
        # )
        btn = self.page.wait_for_selector(selector=".FilterGroup__toggle")
        if btn:
            btn.click()
        else:
            logger.error("Кнопки нет")
        # temp = self.page.wait_for_selector(selector=".filter-region__item")
        cities_block = self.page.evaluate(expression=GET_AREAS)
        breakpoint()
        time.sleep(30)


if __name__ == "__main__":
    with ChromeBrowser(headless=False) as browser:
        browser.start_parsing(url="https://kolesa.kz/cars/astana/")
