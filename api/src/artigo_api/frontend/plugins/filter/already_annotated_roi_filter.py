import logging

from frontend.models import UserROI
from frontend.plugins import (
    FilterPlugin,
    FilterPluginManager,
)
from frontend.utils import get_iou
from frontend.serializers import TagROISerializer

logger = logging.getLogger(__name__)


@FilterPluginManager.export('AlreadyAnnotatedROIFilter')
class AlreadyAnnotatedROIFilter(FilterPlugin):
    default_config = {
        'iou_value': 0.5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.iou_value = self.config['iou_value']

    def __call__(self, tags, gameround, params):
        invalid_tags = UserROI.objects.filter(
                gameround=gameround,
                resource=gameround.resource,
            ) \
            .values(
                'tag__name',
                'x',
                'y',
                'width',
                'height',
            )

        invalid_tags = TagROISerializer(invalid_tags, many=True).data
        invalid_tags = {x['tag_name']: x['data'] for x in invalid_tags}

        for tag in tags:
            for roi in invalid_tags.get(tag['name'], []):
                if tag['valid'] and get_iou(tag, roi) >= self.iou_value:
                    tag['valid'] = False
                    break
