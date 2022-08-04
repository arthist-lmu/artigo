import logging

from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import Coalesce
from frontend.models import Resource

logger = logging.getLogger(__name__)


def name(func=None):
    def wrapper(*args, **kwargs):
        try:
            name = func.__func__.__qualname__
        except:
            name = func.__qualname__

        return func(*args, **kwargs, name=name)

    return wrapper


@name
def resource_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        values = Resource.objects.latest('id').id

        timeout = kwargs.get('timeout', 60 * 60 * 24)
        cache.set(kwargs['name'], values, timeout)

    return values


@name
def resource_tagging_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        values = Resource.objects.values('id') \
            .exclude(hash_id__exact='') \
            .annotate(
                count_tags=Coalesce(Count('taggings__tag', distinct=True), 0),
                count_taggings=Coalesce(Count('taggings__tag'), 0),
                count_roi_tags=Coalesce(Count('rois__tag', distinct=True), 0),
                count_roi_taggings=Coalesce(Count('rois__tag'), 0),
            )

        timeout = kwargs.get('timeout', 60 * 60 * 24)
        cache.set(kwargs['name'], values, timeout)

    return values
