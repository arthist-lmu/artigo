import logging

from django.db.models import Count
from frontend.models import UserTagging
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)
from frontend.utils import to_iregex

logger = logging.getLogger(__name__)


@ScorePluginManager.export('TagFirstAnnotationScore')
class TagFirstAnnotationScore(ScorePlugin):
    default_config = {
        'point_value': 5,
        'min_taggings': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.point_value = self.config['point_value']
        self.min_taggings = self.config['min_taggings']

    def __call__(self, tags, gameround, params):
        users = UserTagging.objects \
            .filter(
                resource=gameround.resource,
                tag__language=params.get('language', 'de'),
            ) \
            .exclude(gameround=gameround) \
            .values_list('user_id', flat=True)

        if len(set(users)) == 0:
            valid_tags = UserTagging.objects.filter(
                    tag__name__iregex=to_iregex(tags, 'name'),
                    tag__language=params.get('language', 'de'),
                ) \
                .values('tag') \
                .annotate(count_taggings=Count('tag')) \
                .filter(count_taggings__gte=self.min_taggings) \
                .values_list('tag__name', flat=True)

            valid_tags = set(x.lower() for x in valid_tags)

            for tag in tags:
                if tag['valid'] and tag['name'] in valid_tags:
                    tag['score'] += self.point_value
