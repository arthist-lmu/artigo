import logging

from frontend.models import OpponentROI
from frontend.plugins import (
    ScorePlugin,
    ScorePluginManager,
)
from frontend.utils import to_iregex, get_iou
from frontend.serializers import TagROISerializer

logger = logging.getLogger(__name__)


@ScorePluginManager.export('OpponentROIValidatedScore')
class OpponentROIValidatedScore(ScorePlugin):
    default_config = {
        'iou_value': 0.5,
        'point_value': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.iou_value = self.config['iou_value']
        self.point_value = self.config['point_value']

    def __call__(self, tags, gameround, params):
        valid_tags = OpponentROI.objects.filter(
                gameround=gameround,
                tag__name__iregex=to_iregex(tags, 'name'),
                tag__language=params.get('language', 'de'),
            ) \
            .values(
                'tag__name',
                'x',
                'y',
                'width',
                'height',
            )

        valid_tags = TagROISerializer(valid_tags, many=True).data
        valid_tags = {x['tag_name']: x['data'] for x in valid_tags}

        for tag in tags:
            for roi in valid_tags.get(tag['name'], []):
                if tag['valid'] and get_iou(tag, roi) >= self.iou_value:
                    tag['score'] += self.point_value
                    break
