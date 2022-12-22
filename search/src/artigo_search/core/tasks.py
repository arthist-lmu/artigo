import os
import logging

from celery import shared_task
from artigo_search.client import Client

logger = logging.getLogger(__name__)
cache = {'count': 0}  # temporary storage


@shared_task()
def import_data():
    try:
        client = Client()
        client.delete()
        client.insert()

        return True
    except:
        pass

    return False


@shared_task(ignore_result=True)
def delete_data(folder='/dump', limit=2):
    files, last_modified = [], lambda file: file.stat().st_mtime

    for file in sorted(os.scandir(folder), key=last_modified, reverse=True):
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

        if result.count == 0 or result.count < cache['count']:
            import_data.delay()

        cache['count'] = result.count

        return result.count
    except:
        pass

    return 0
