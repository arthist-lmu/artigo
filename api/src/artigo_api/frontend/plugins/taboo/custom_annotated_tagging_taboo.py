import logging

from frontend.models import Tag
from frontend.plugins import (
    TabooPlugin,
    TabooPluginManager,
)

logger = logging.getLogger(__name__)


@TabooPluginManager.export('CustomAnnotatedTaggingTaboo')
class CustomAnnotatedTaggingTaboo(TabooPlugin):
    default_config = {
        'inputs': [],
        'max_tags': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.inputs = self.config['inputs']
        self.max_tags = self.config['max_tags']

        if not isinstance(self.inputs, (list, set)):
            self.inputs = [self.inputs]

    def __call__(self, resource_ids, params):
        tags = [{'name': tag} for tag in self.inputs]

        for tag in tags:
            tag_obj = Tag.objects.filter(
                name__iexact=tag['name'],
                language=params.get('language', 'de'),
            ).first()

            if tag_obj is None:
                tag_obj = Tag.objects.create(
                    name=tag['name'],
                    language=params.get('language', 'de'),
                )

            tag['id'] = tag_obj.id

        return [
            {
                'resource_id': resource_id,
                'tags': tags[:self.max_tags],
            }
            for resource_id in resource_ids
        ]
