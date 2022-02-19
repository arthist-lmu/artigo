import json
import logging

from urllib import parse
from artigo_search.plugins import (
    ReconciliatorPlugin,
    ReconciliatorPluginManager,
)

logger = logging.getLogger(__name__)


@ReconciliatorPluginManager.export('WikidataReconciliator')
class WikidataReconciliator(ReconciliatorPlugin):
    default_config = {
        'endpoint': 'https://wikidata.reconci.link/{}/api',
        'params': {
            'limit': 5,
            'timeout': 20000,
        },
        'lang': 'en',
        'creator_type': 'Q5',
        'resource_type': 'Q838948',
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.endpoint = self.config['endpoint']
        self.params = self.config['params']
        self.lang = self.config['lang']

        self.creator_type = self.config['creator_type']
        self.resource_type = self.config['resource_type']

    def __call__(self, query, size=5):
        if size is not None and isinstance(size, int):
            self.params['limit'] = size

        lang = query.get('lang', self.lang)
        endpoint = self.endpoint.format(lang)

        query = self.parse_query(query)
        urls = self.parse_url(endpoint, query)

        for _, entries in self.harvest(list(urls)):
            for entry in entries:
                yield entry

    def parse_query(self, query):
        queries = {}

        for i, term in enumerate(query['terms']):
            if term['type'] == 'creator':
                term['type'] = self.creator_type
            elif term['type'] == 'resource':
                term['type'] = self.resource_type
            else:
                continue

            queries[f'q{i}'] = {
                'query': term['name'],
                'type': term['type'],
            }

        return dict(
            {'queries': queries},
            **self.params,
        )

    def extract(self, url, response):
        entries = []

        for results in json.loads(response).values():
            for result in results['result']:
                entries.append({
                    'id': result['id'],
                    'name': result['name'],
                    'description': result['description'],
                    'score': int(result['score']),
                    'match': result['match'],
                    'service': 'Wikidata',
                })

        return url, entries
