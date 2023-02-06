import logging

from django.db.models import Count
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

        self.model = UserTagging
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
        resources = self.exclude_last_played(resources, params)
        resources = self.filter_collections(resources, params)

        resource_ids = random_resources(resources, self.rounds)

        return resource_ids
