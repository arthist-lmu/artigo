import logging

from django.db.models import Count
from frontend.models import OpponentTagging
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)

logger = logging.getLogger(__name__)


@ScorePluginManager.export('OpponentValidatedScore')
class OpponentValidatedScore(ScorePlugin):
    default_config = {
        'point_value': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.point_value = self.config['point_value']

    def __call__(self, tags, gameround, params):
        valid_tags = OpponentTagging.objects.filter(
                gameround=gameround,
                tag__name__iregex=f"({'|'.join(tags)})",
                tag__language=params.get('language', 'de'),
            ) \
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
