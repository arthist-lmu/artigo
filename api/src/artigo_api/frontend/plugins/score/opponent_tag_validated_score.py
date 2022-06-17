import logging

from frontend.models import OpponentTagging
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)
from frontend.utils import to_iregex

logger = logging.getLogger(__name__)


@ScorePluginManager.export('OpponentTagValidatedScore')
class OpponentTagValidatedScore(ScorePlugin):
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
                tag__name__iregex=to_iregex(tags, 'name'),
                tag__language=params.get('language', 'de'),
            ) \
            .values_list('tag__name', flat=True)

        valid_tags = set(x.lower() for x in valid_tags)

        for tag in tags:
            tag['score'] = tag.get('score', 0)

            if tag['valid'] and tag['name'] in valid_tags:
                tag['score'] += self.point_value
