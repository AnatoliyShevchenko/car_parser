from loguru import logger
from django.core.management.base import BaseCommand
import requests
from PIL import Image

from modules.browser import ChromeBrowser
from car_adverts.models import Advert, AdvertImage


class Command(BaseCommand):
    def get_data(self, advert_id: int):
        with ChromeBrowser() as browser:
            links = browser.collect_links(advert_id=advert_id)
        return links
    
    def processing_link(self, link: str) -> bytes | None:
        try:
            response = requests.get(url=link)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Cannot open image: {e}")
            return None
    
    def handle(self, *args, **options):
        adverts = Advert.objects.filter(advert_images__isnull=True)
        for advert in adverts[:5]:
            links = self.get_data(advert_id=advert.pk)
            for link in links:
                img_bytes = self.processing_link(link=link)
                if not img_bytes:
                    continue
                image = Image.open(img_bytes)
