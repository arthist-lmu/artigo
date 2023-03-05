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


@ResourcePluginManager.export('CustomROIResource')
class CustomROIResource(ResourcePlugin):
    default_config = {
        'inputs': [],
        'rounds': 5,
        'min_tags': 5,
        'min_roi_tags': 0,
        'max_last_played': 0,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = UserROI
        self.inputs = self.config['inputs']
        self.rounds = self.config['rounds']
        self.min_tags = self.config['min_tags']
        self.min_roi_tags = self.config['min_roi_tags']
        self.max_last_played = self.config['max_last_played']

        if not isinstance(self.inputs, (list, set)):
            self.inputs = [self.inputs]

    def __call__(self, params):
        resources = cache.resource_tagging_count(**params) \
            .filter(
                id__in=self.inputs[:100],
                count_tags__gte=self.min_tags,
                count_roi_tags__gte=self.min_roi_tags,
            )

        resources = self.exclude_last_played(resources, params)
        resources = self.filter_collections(resources, params)

        resource_ids = list(resources.values_list('id', flat=True))

        self.rounds = min(len(resource_ids), self.rounds)
        resource_ids = random.sample(resource_ids, max(1, self.rounds))

        return resource_ids
