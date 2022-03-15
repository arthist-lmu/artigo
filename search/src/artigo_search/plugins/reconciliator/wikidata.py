import json
import logging

from urllib import parse
from itertools import islice
from collections import defaultdict
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
            'timeout': 20000,
        },
        'lang': 'en',
        'creator_type': 'Q5',
        'resource_type': 'Q838948',
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mapper = defaultdict(set)

        self.endpoint = self.config['endpoint']
        self.params = self.config['params']
        self.lang = self.config['lang']

        self.creator_type = self.config['creator_type']
        self.resource_type = self.config['resource_type']

    def __call__(self, query, size=5):
        lang = query.get('lang', self.lang)
        endpoint = self.endpoint.format(lang)

        query = self.parse_query(query, size)
        urls = self.parse_url(endpoint, query)

        for _, entries in self.harvest(list(urls)):
            for entry in entries:
                yield entry

    def parse_query(self, query, size, n=10):
        queries = {}

        for term in query['terms']:
            key = f'{term["type"]}:{term["name"]}'

            if term.get('id'):
                self.mapper[key].add(term['id'])

            if term['type'] == 'creator':
                term['type'] = self.creator_type
            elif term['type'] == 'resource':
                term['type'] = self.resource_type
            else:
                continue

            queries[key] = {
                'query': term['name'],
                'type': term['type'],
                'limit': size,
            }

        if n > 0:
            iter_queries = iter(queries)

            for _ in range(0, len(queries), n):
                query_chunk = {
                    key: queries[key]
                    for key in islice(iter_queries, n)
                }

                yield dict(
                    {'queries': query_chunk},
                    **self.params,
                )

    def extract(self, url, response):
        reconciliations = []

        for key, x in json.loads(response).items():
            values = {
                'name': key.split(':', 1)[1],
                'type': key.split(':', 1)[0],
                'service': 'Wikidata',
                'entries': [],
            }

            if self.mapper.get(key):
                values['ids'] = self.mapper[key]

            for result in x['result']:
                values['entries'].append({
                    'id': result['id'],
                    'name': result['name'],
                    'description': result['description'],
                    'score': int(result['score']),
                })

            reconciliations.append(values)

        return url, reconciliations
