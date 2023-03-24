import os
import logging

from celery import shared_task
from artigo_search.client import Client

logger = logging.getLogger(__name__)


@shared_task(acks_late=True, reject_on_worker_lost=True)
def import_data():
    try:
        client = Client()
        client.delete()
        client.insert()

        return True
    except Exception as error:
        raise self.retry(exc=error, countdown=5)


@shared_task(ignore_result=True)
def delete_data(folder='/dump', limit=2):
    files = []

    for file in sorted(
        os.scandir(folder),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    ):
        if file.name.startswith('os-dump_'):
            file_path = os.path.join(folder, file.name)

            if len(files) < limit:
                files.append(file_path)
            else:
                os.remove(file_path)


@shared_task()
def document_count():
    try:
        result = Client().count()

        if result.count == 0:
            import_data.delay()

        return result.count
    except:
        pass

    return 0
