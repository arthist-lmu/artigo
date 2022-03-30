import logging

from django.db.models import Count
from frontend.models import UserTagging
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)

logger = logging.getLogger(__name__)


@ScorePluginManager.export('AnnotationValidatedScore')
class AnnotationValidatedScore(ScorePlugin):
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
                resource_id=params.get('resource_id'),
                tag__name__iregex=f"({'|'.join(tags)})",
                tag__language=params.get('language', 'de'),
            ) \
            .values('resource', 'tag') \
            .annotate(count_taggings=Count('tag')) \
            .filter(count_taggings__gte=self.min_taggings) \
            .values_list('tag__name', flat=True)

        valid_tags = set(x.lower() for x in valid_tags)

        result = []

        for tag in tags:
            is_valid = tag in valid_tags

            result.append({
                'name': tag,
                'score': is_valid * self.point_value,
            })

        return result
