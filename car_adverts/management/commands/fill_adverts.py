from loguru import logger
from django.core.management.base import BaseCommand

from modules.browser import ChromeBrowser
from car_adverts.models import Advert


class Command(BaseCommand):
    def processing(self, advert_id: int):
        with ChromeBrowser(headless=False) as browser:
            data = browser.get_full_data(advert_id=advert_id)
        return data

    def handle(self, *args, **options):
        adverts = Advert.objects.filter(title__isnull=True)
        if not adverts:
            logger.info("There are no adverts to processing")
            return
        logger.info(f"Founded {len(adverts)} adverts")
        for advert in adverts:
            data = self.processing(advert_id=advert.pk)
            if not data:
                continue
