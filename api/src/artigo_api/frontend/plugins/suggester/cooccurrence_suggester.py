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
        return list(AggregateView()(tags, self.config))


class AggregateView(AggregateViewHelper):
    def __call__(self, tags, config):
        for tag in tags:
            params = {
                'query': [{
                    'name': 'tags',
                    'value': tag,
                }],
                'aggregate': {
                    'use_query': True,
                    'fields': ['tags'],
                    'size': config.get('max_tags', 10) + 1,
                    'significant': True,
                },
            }

            result = self.rpc_post(params)

            for aggregation in result['aggregations']:
                for entry in aggregation['entries']:
                    yield {
                        'name': tag,
                        'suggest': entry['name'],
                    }
