import time
import random
from datetime import datetime, date

import requests
from bs4 import BeautifulSoup, Tag
from loguru import logger
from fake_useragent import UserAgent

MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


class AdvertsCollector:
    def __init__(
        self, date: date, city_alias: str, max_attempts: int = 3
    ):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "referer": "https://kolesa.kz/",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24",\
             "Microsoft Edge";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "x-requested-with": "XMLHttpRequest",
        }
        self.date = date
        self.city = city_alias
        self.max_attempts = max_attempts if max_attempts > 1 else 3
        self.base_url = "https://kolesa.kz/cars/"

    def data_processing(self, content: bytes) -> list:
        soup = BeautifulSoup(markup=content)
        car_list: list[Tag] = soup.find_all(
            name="div",
            attrs={"class": "a-card js__a-card"},
        )
        adverts = []
        for item in car_list:
            advert_id: str = item.attrs.get("data-id")
            public_date: str = item.find(
                name="span",
                attrs={"class": "a-card__param a-card__param--date"},
            ).get_text()
            try:
                day, month = public_date.split(" ")
            except Exception as e:
                logger.debug(f"Something went wrong: {e}")
                continue
            date_to_compare = date(
                year=datetime.now().year,
                month=MONTHS.get(month),
                day=int(day),
            )
            if date_to_compare < self.date:
                continue
            adverts.append((int(advert_id), date_to_compare))
        return adverts

    def run(self):
        adverts = []
        while True:
            page = 1
            self.headers["user-agent"] = UserAgent().random
            url = f"{self.base_url}{self.city}/?page={page}"
            try:
                logger.debug(f"Make request url: {url}")
                response = requests.get(url=url, headers=self.headers)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Something happened: {e}")
                return
            content = response.content
            if not content:
                continue
            data = self.data_processing(content=content)
            if not data:
                break
            adverts.extend(data)
            page += 1
            delay = random.randint(3, 6)
            logger.debug(f"Sleep for {delay} seconds")
            time.sleep(random.randint(3, 6))
        return adverts


if __name__ == "__main__":
    collector = AdvertsCollector(
        date=date(year=2025, month=8, day=28),
        city_alias="region-karagandinskaya-oblast",
    )
    logger.info(f"Data: {collector.run()}")
