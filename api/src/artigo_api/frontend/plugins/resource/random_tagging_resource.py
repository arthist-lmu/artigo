import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils.timezone import make_aware
from frontend import cache
from frontend.models import UserTagging
from frontend.functions import Percentile
from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)
from .utils import random_resources

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('RandomTaggingResource')
class RandomTaggingResource(ResourcePlugin):
    default_config = {
        'rounds': 5,
        'min_tags': 5,
        'percentile': 1.0,
        'max_last_played': 6 * 30,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rounds = self.config['rounds']
        self.min_tags = self.config['min_tags']
        self.percentile = self.config['percentile']
        self.max_last_played = self.config['max_last_played']

    def __call__(self, params):
        resources = cache.resource_tagging_count()

        if self.percentile < 1:
            value = resources.aggregate(
                x=Percentile('count_taggings', p=self.percentile),
            )
            resources = resources.filter(count_taggings__lt=value['x'])

        resources = resources.filter(count_tags__gte=self.min_tags)

        if params.get('user_id') and self.max_last_played > 0:
            max_last_played = make_aware(datetime.today()) \
                - relativedelta(days=self.max_last_played)

            user_resources = UserTagging.objects.filter(user_id=params['user_id']) \
                .filter(created__gt=max_last_played) \
                .values('resource')

            resources = resources.exclude(id__in=user_resources)

        resource_ids = random_resources(resources, limit=self.rounds)

        return resource_ids
