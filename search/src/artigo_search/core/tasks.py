import os
import logging

from celery import shared_task
from artigo_search.client import Client

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def import_jsonl():
    client = Client()
    client.delete()
    client.insert()


@shared_task(ignore_result=True)
def delete_jsonl(folder='/dump', limit=2):
    files, last_modified = [], lambda file: file.stat().st_mtime

    for file in sorted(os.scandir(folder), key=last_modified, reverse=True):
        if file.name.startswith('os-dump_'):
            file_path = os.path.join(folder, file.name)

            if len(files) < limit:
                files.append(file_path)
            else:
                os.remove(file_path)
