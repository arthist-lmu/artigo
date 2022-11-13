import logging

from django.core.cache import cache
from frontend.models import Resource
from .utils import name

logger = logging.getLogger(__name__)


@name
def resource_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        values = Resource.objects.latest('id').id

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
