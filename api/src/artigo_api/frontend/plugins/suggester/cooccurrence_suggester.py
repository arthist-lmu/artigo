import time
import logging

from frontend.plugins import (
    SuggesterPlugin,
    SuggesterPluginManager,
)
from frontend.views.utils import AggregateViewHelper

logger = logging.getLogger(__name__)


@SuggesterPluginManager.export('CooccurrenceSuggester')
class CooccurrenceSuggester(SuggesterPlugin):
    default_config = {
        'max_tags': 10,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max_tags = self.config['max_tags']

    def __call__(self, tags, params):
        AggregateView()(tags, self.max_tags)


class AggregateView(AggregateViewHelper):
    def __call__(self, tags, max_tags):
        for tag in tags:
            if tag['suggested']:
                continue

            if not tag.get('suggest'):
                tag['suggest'] = set()

            params = {
                'query': [{
                    'name': 'tags',
                    'value': tag['name'],
                }],
                'aggregate': {
                    'use_query': True,
                    'fields': ['tags'],
                    'size': max_tags + 1,
                    'significant': True,
                },
            }

            result = self.rpc_post(params)

            for aggregation in result['aggregations']:
                for entry in aggregation['entries']:
                    if entry['name'] != tag['name']:
                        tag['suggest'].add(entry['name'])

        return tags
