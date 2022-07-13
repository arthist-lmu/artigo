import logging

from django.db.models import Count
from frontend.models import Tag, UserTagging
from frontend.plugins import (
    TabooPlugin,
    TabooPluginManager,
)
from frontend.serializers import TabooTagSerializer

logger = logging.getLogger(__name__)


@TabooPluginManager.export('RandomAnnotatedTaggingTaboo')
class RandomAnnotatedTaggingTaboo(TabooPlugin):
    default_config = {
        'max_tags': 5,
        'is_validated': True,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max_tags = self.config['max_tags']
        self.is_validated = self.config['is_validated']

    def __call__(self, resource_ids, params):
        min_taggings = 2 if self.is_validated else 0

        taggings = UserTagging.objects.filter(
                resource_id__in=resource_ids,
                tag__language=params.get('language', 'de'),
            ) \
            .values('resource', 'tag') \
            .annotate(count_taggings=Count('tag')) \
            .filter(count_taggings__gte=min_taggings) \
            .order_by('resource', '?') \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
            )

        taboos = TabooTagSerializer(taggings, many=True).data

        for taboo in taboos:
            taboo['tags'] = taboo['tags'][:self.max_tags]

        return taboos
