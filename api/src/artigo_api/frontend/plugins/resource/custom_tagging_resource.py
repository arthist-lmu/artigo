import random
import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from frontend import cache
from frontend.models import UserTagging
from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('CustomTaggingResource')
class CustomTaggingResource(ResourcePlugin):
    default_config = {
        'inputs': [],
        'rounds': 5,
        'min_tags': 5,
        'max_last_played': 0,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.inputs = self.config['inputs']
        self.rounds = self.config['rounds']
        self.min_tags = self.config['min_tags']
        self.max_last_played = self.config['max_last_played']

        if not isinstance(self.inputs, (list, set)):
            self.inputs = [self.inputs]

    def __call__(self, params):
        resources = cache.resource_tagging_count() \
            .filter(
                id__in=self.inputs[:100],
                count_tags__gte=self.min_tags,
            )

        if params.get('user_id') and self.max_last_played > 0:
            max_last_played = make_aware(datetime.today()) \
                - relativedelta(days=self.max_last_played)

            user_resources = UserTagging.objects \
                .filter(user_id=params['user_id']) \
                .filter(created__gt=max_last_played) \
                .values('resource')

            resources = resources.exclude(id__in=user_resources)

        resource_ids = list(resources.values_list('id', flat=True))
        
        self.rounds = min(len(resource_ids), self.rounds)
        resource_ids = random.sample(resource_ids, max(1, self.rounds))

        return resource_ids
