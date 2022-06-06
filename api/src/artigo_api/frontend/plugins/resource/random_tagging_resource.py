import random
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
        if params.get('id'):
            if not isinstance(params['id'], (list, set)):
                params['id'] = [params['id']]

            resources = UserTagging.objects.values('resource') \
                .filter(resource__id__in=params['id']) \
                .exclude(resource__hash_id__exact='') \
                .annotate(
                    count_tags=Count('tag', distinct=True),
                    count_taggings=Count('tag'),
                )
        else:
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

            resources = resources.exclude(resource__in=user_resources)

        if params.get('id'):
            resource_ids = list(resources.values_list('resource_id', flat=True))
            resource_ids = random.sample(resource_ids, max(1, self.rounds))
        else:
            # TODO: test efficiency for larger numbers of gamerounds
            resource_ids = set()

            while True:
                i = random.randint(0, cache.resource_count() - 1)

                try:
                    resource_ids.add(resources.get(resource=i)['resource'])
                except:
                    pass

                if len(resource_ids) == self.rounds:
                    break

        return list(resource_ids)
