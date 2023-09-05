import os
import logging

from io import StringIO
from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)


def get_file_size_in_mb(file_path):
    try:
        file_path = file_path.getvalue().strip()
    except:
        pass
        
    file_size = os.path.getsize(file_path)

    return file_size / 1024 ** 2


@shared_task()
def export_data():
    file_path_aggregate = StringIO()
    file_path_raw = StringIO()

    call_command(
        'export_data_aggregate',
        format='jsonl',
        output='/dump',
        stdout=file_path_aggregate,
    )

    call_command(
        'export_data_raw',
        format='jsonl',
        output='/dump',
        exclude=[
            'auth',
            'admin',
            'account',
            'contenttypes',
        ],
        stdout=file_path_raw,
    )

    return {
        'file_size_aggregate': get_file_size_in_mb(file_path_aggregate),
        'file_size_raw': get_file_size_in_mb(file_path_raw)
    }


@shared_task(ignore_result=True)
def delete_data():
    call_command(
        'delete_data',
        input='/dump',
        limit=2,
    )


@shared_task(ignore_result=True)
def upload_data():
    call_command(
        'upload_data',
        dump_input='/dump',
        media_input='/media',
        zenodo='publish',
    )
