import logging

from django.db.models import Count
from frontend.models import UserTagging
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)
from frontend.utils import to_iregex

logger = logging.getLogger(__name__)


@ScorePluginManager.export('TagValidatedScore')
class TagValidatedScore(ScorePlugin):
    default_config = {
        'point_value': 5,
        'min_taggings': 1,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.point_value = self.config['point_value']
        self.min_taggings = self.config['min_taggings']

    def __call__(self, tags, gameround, params):
        valid_tags = UserTagging.objects.filter(
                resource=gameround.resource,
                tag__name__iregex=to_iregex(tags, 'name'),
                tag__language=params.get('language', 'de'),
            ) \
            .exclude(user=gameround.user) \
            .values('resource', 'tag') \
            .annotate(count_taggings=Count('tag')) \
            .filter(count_taggings__gte=self.min_taggings) \
            .values_list('tag__name', flat=True)

        valid_tags = set(x.lower() for x in valid_tags)

        for tag in tags:
            tag['score'] = tag.get('score', 0)

            if tag['valid'] and tag['name'] in valid_tags:
                tag['score'] += self.point_value
