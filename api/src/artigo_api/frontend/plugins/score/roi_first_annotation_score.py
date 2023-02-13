import logging

from frontend.models import UserROI
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)

logger = logging.getLogger(__name__)


@ScorePluginManager.export('ROIFirstAnnotationScore')
class ROIFirstAnnotationScore(ScorePlugin):
    default_config = {
        'point_value': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.point_value = self.config['point_value']

    def __call__(self, tags, gameround, params):
        users = UserROI.objects \
            .filter(resource=gameround.resource) \
            .exclude(gameround=gameround) \
            .values_list('user_id', flat=True)

        if len(set(users)) == 0:
            for tag in tags:
                if tag['valid']:
                    tag['score'] += self.point_value
