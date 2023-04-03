import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def export_data():
    call_command(
        'export_data',
        format='jsonl',
        output='/dump',
    )


@shared_task(ignore_result=True)
def upload_data():
    call_command(
        'upload_data',
        dump_input='/dump',
        media_input='/media',
        publish=True,
    )
