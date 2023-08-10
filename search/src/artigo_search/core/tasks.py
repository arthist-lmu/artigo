import os
import logging

from celery import shared_task
from artigo_search.client import Client

logger = logging.getLogger(__name__)


@shared_task(bind=True, acks_late=True, reject_on_worker_lost=True)
def import_data(self):
    try:
        client = Client()
        client.delete()
        client.insert()

        return True
    except Exception as error:
        raise self.retry(exc=error, countdown=5)


@shared_task()
def document_count():
    try:
        result = Client().count()

        if result.count == 0:
            import_data.delay()

        return result.count
    except:
        pass

    return -1
