import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def export_data():
    call_command('export', format='jsonl', output='/dump')
