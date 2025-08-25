import time

from playwright.sync_api import sync_playwright
from loguru import logger

from modules.scripts import GET_AREAS


# GET_AREAS = """
# const regions = [];

# window.document.querySelectorAll('li.filter-region__item').forEach(li => {
#     const btn = li.querySelector('button');
#     const alias = btn.getAttribute('data-alias');
#     const label = li.innerText;

#     if (label) {
#         regions.push({ alias, label });
#     }
# });
# regions;
# """


class ChromeBrowser:
    def __init__(self, headless: bool = True):
        self.base_url = "https://kolesa.kz/cars/"
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

    def get_cities(self):
        self.page.goto(url=self.base_url)
        # more_btn = self.page.locator(selector=".FilterGroup__toggle")
        # self.page.evaluate(
        #     expression="window.document.querySelector('.FilterGroup__toggle').click()"
        # )
        btn = self.page.wait_for_selector(selector=".FilterGroup__toggle")
        if btn:
            btn.click()
        else:
            logger.error("Кнопки нет")
        time.sleep(3)
        # temp = self.page.wait_for_selector(selector=".filter-region__item")
        cities_block = self.page.evaluate(expression=GET_AREAS)
        return cities_block


if __name__ == "__main__":
    with ChromeBrowser(headless=False) as browser:
        browser.get_cities()
