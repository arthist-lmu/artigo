import logging

from django.utils import timezone
from django.core.management import BaseCommand
from frontend import cache

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--renew', action='store_true')

    def handle(self, *args, **options):
        start_time = timezone.now()

        for name in dir(cache):
            item = getattr(cache, name)

            if callable(item):
                try:
                    item(renew=options['renew'])
                except:
                    pass

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Renew took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
