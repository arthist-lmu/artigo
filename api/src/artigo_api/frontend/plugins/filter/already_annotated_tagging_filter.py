import logging

from frontend.models import UserTagging
from frontend.plugins import (
    FilterPlugin,
    FilterPluginManager,
)

logger = logging.getLogger(__name__)


@FilterPluginManager.export('AlreadyAnnotatedTaggingFilter')
class AlreadyAnnotatedTaggingFilter(FilterPlugin):
    default_config = {}
    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tags, gameround, params):
        invalid_tags = UserTagging.objects.filter(
                gameround=gameround,
                resource=gameround.resource,
            ) \
            .values_list('tag__name', flat=True)

        invalid_tags = set(x.lower() for x in invalid_tags)

        for tag in tags:
            if tag['valid'] and tag['name'] in invalid_tags:
                tag['valid'] = False
