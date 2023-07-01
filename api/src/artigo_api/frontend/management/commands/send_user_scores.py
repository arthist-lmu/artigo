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
        result = cache.user_scores()['scores']

        send_mail(
            'Monthly user scores are updated',
            message=json.dumps(result['previous_month']),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
