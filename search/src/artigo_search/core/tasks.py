import os
import logging

from celery import shared_task
from artigo_search.client import Client

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={
        'max_retries': 3,
        'countdown': 5,
    },
)
def import_data(self):
    client = Client()
    client.delete()
    client.insert()

    return True


@shared_task()
def document_count():
    try:
        client = Client()
        result = client.count()

        if result.count == 0:
            import_data.delay()

        return result.count
    except:
        pass

    return -1
