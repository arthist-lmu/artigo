import random
import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import make_aware
from frontend.models import Tagging
from frontend.functions import Percentile
from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('RandomResource')
class RandomResource(ResourcePlugin):
    default_config = {
        'rounds': 5,
        'min_tags': 5,
        'lt_percentile': 1.0,
        'max_last_played': 6 * 30,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cache = {
            'name': 'resource_tag_count',
            'timeout': 60 * 60 * 12,
        }

        self.rounds = self.config['rounds']
        self.min_tags = self.config['min_tags']
        self.lt_percentile = self.config['lt_percentile']
        self.max_last_played = self.config['max_last_played']

    def __call__(self, params):
        resources = cache.get(self.cache['name'])

        if resources is None:
            resources = Tagging.objects.values('resource') \
                .annotate(
                    count_tags=Count('tag', distinct=True),
                    count_taggings=Count('tag'),
                )

            cache.set(self.cache['name'], resources, self.cache['timeout'])

        if self.lt_percentile < 1:
            value = resources.aggregate(
                x=Percentile('count_taggings', p=self.lt_percentile),
            )
            resources = resources.filter(count_taggings__lt=value['x'])

        resources = resources.filter(
            count_tags__gte=self.min_tags,
            tag__language=params.get('language', 'de'),
        )

        if params.get('user_id') and self.max_last_played > 0:
            max_last_played = make_aware(datetime.today()) \
                - relativedelta(days=self.max_last_played)

            user_resources = Tagging.objects.filter(user_id=params['user_id']) \
                .filter(created__gt=max_last_played) \
                .values('resource')

            resources = resources.exclude(resource__in=user_resources)
        
        resources = resources.order_by('?')[:max(1, self.rounds)]

        return resources.values_list('resource_id', flat=True)
