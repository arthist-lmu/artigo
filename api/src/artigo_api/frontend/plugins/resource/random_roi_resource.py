import random
import logging

from django.db.models import Count
from frontend import cache
from frontend.models import UserROI
from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)
from .utils import random_resources

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('RandomROIResource')
class RandomROIResource(ResourcePlugin):
    default_config = {
        'rounds': 5,
        'min_tags': 5,
        'min_roi_tags': 0,
        'max_last_played': 6 * 30,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = UserROI
        self.rounds = self.config['rounds']
        self.min_tags = self.config['min_tags']
        self.min_roi_tags = self.config['min_roi_tags']
        self.max_last_played = self.config['max_last_played']

    def __call__(self, params):
        resources = cache.resource_tagging_count(**params) \
            .filter(
                count_tags__gte=self.min_tags,
                count_roi_tags__gte=self.min_roi_tags
            )

        resources = self.exclude_last_played(resources, params)
        resources = self.filter_collections(resources, params)
        
        resource_ids = random_resources(resources, self.rounds)

        return resource_ids
