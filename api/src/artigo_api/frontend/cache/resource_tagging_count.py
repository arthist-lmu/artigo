import logging

from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from frontend.models import Resource
from .utils import name

logger = logging.getLogger(__name__)


@name
def resource_tagging_count(**kwargs):
    langs = kwargs.get('language', ['de', 'en'])

    if not isinstance(langs, (list, set)):
        langs = [langs]

    for lang in langs:
        cache_name = f"{kwargs['name']}_{lang}"
        values = cache.get(cache_name)

        if values is None or kwargs.get('renew'):
            values = Resource.objects.values('id') \
                .exclude(hash_id__exact='') \
                .annotate(
                    count_tags=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__language=lang),
                            distinct=True
                        ), 
                        0,
                    ),
                    count_taggings=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__language=lang),
                        ),
                        0,
                    ),
                    count_roi_tags=Coalesce(
                        Count(
                            'rois__tag',
                            filter=Q(rois__tag__language=lang),
                            distinct=True,
                        ),
                        0,
                    ),
                    count_roi_taggings=Coalesce(
                        Count(
                            'rois__tag',
                            filter=Q(rois__tag__language=lang),
                        ),
                        0,
                    ),
                )

            timeout = kwargs.get('timeout', None)
            cache.set(cache_name, values, timeout)

    return values
