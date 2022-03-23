import logging

from frontend.models import Tagging
from frontend.plugins import (
    FilterPlugin,
    FilterPluginManager,
)

logger = logging.getLogger(__name__)


@FilterPluginManager.export('AlreadyAnnotatedFilter')
class AlreadyAnnotatedFilter(FilterPlugin):
    default_config = {}
    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tags, gameround, params):
        invalid_tags = Tagging.objects.filter(
                gameround=gameround,
                resource=gameround.resource,
            ) \
            .values_list('tag__name', flat=True)

        invalid_tags = set(x.lower() for x in invalid_tags)

        result = []

        for tag in tags:
            result.append({
                'name': tag,
                'valid': tag not in invalid_tags,
            })
            
        return result
