import logging

from frontend import cache
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def renew_cache():
    for name in dir(cache):
        item = getattr(cache, name)

        if callable(item):
            try:
                item(renew=True)
            except:
                pass
