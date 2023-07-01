import json
import logging
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from frontend import cache

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        results = cache.user_scores()['scores']['previous_month']

        for i, result in enumerate(results):
            results[i] = f'{i + 1}. ' + \
                f'E-Mail: {result["email"]} (' + \
                f'Score: {result["sum_score"]}, ' + \
                f'Taggings: {result["sum_count"]})'

        send_mail(
            'Monthly user scores are updated',
            message='\n'.join(results),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
