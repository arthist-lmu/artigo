import logging

from django.db.models import Count
from frontend.models import Tagging
from frontend.plugins import (
    TabooPlugin,
    TabooPluginManager,
)
from frontend.serializers import TabooSerializer

logger = logging.getLogger(__name__)


@TabooPluginManager.export('MostAnnotatedTaboo')
class MostAnnotatedTaboo(TabooPlugin):
    default_config = {
        'max_tags': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max_tags = self.config['max_tags']

    def __call__(self, resource_ids, params):
        taggings = Tagging.objects.filter(
                resource_id__in=resource_ids,
                tag__language=params.get('language', 'de'),
            ) \
            .values('resource', 'tag') \
            .annotate(count_taggings=Count('tag')) \
            .order_by('resource', 'count_taggings', '?') \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
            )

        taboos = TabooSerializer(taggings, many=True).data

        for taboo in taboos:
            taboo['tags'] = taboo['tags'][:self.max_tags]

        return taboos
