import uuid
import logging

from opensearchpy import OpenSearch, exceptions
from opensearchpy.helpers import bulk
from opensearch_dsl import Search, Q

logger = logging.getLogger(__name__)


class Backbone:
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 9200)

        self.client = OpenSearch(
            [{'host': self.host, 'port': self.port}],
            http_compress=True, ssl_show_warn=False,
            use_ssl=False, ssl_assert_hostname=False, 
        )

        self.index = config.get('index', 'artigo')
        self.type = config.get('type', '_doc')

        if not self.client.indices.exists(index=self.index):
            body = {
                'mappings': {
                    'properties': {
                        'id': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256,
                                },
                            },
                        },
                        'path': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256,
                                },
                            },
                        },
                        'meta': {
                            'type': 'nested',
                            'properties': {
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        },
                                    },
                                },
                                'value_str': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        }
                                    },
                                    'copy_to': ['all_text', 'all_meta'],
                                },
                                'value_int': {
                                    'type': 'long',
                                },
                                'value_float': {
                                    'type': 'float',
                                },
                            },
                        },
                        'tags': {
                            'type': 'nested',
                            'properties': {
                                'id': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        },
                                    },
                                },
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        }
                                    },
                                    'copy_to': ['all_text'],
                                },
                                'count': {
                                    'type': 'long',
                                }
                            }
                        },
                        'source': {
                            'type': 'nested',
                            'properties': {
                                'id': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        },
                                    },
                                },
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        },
                                    },
                                },
                                'url': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256,
                                        },
                                    },
                                },
                                'is_public': {
                                    'type': 'boolean',
                                },
                            },
                        },
                        'all_text': {
                            'type': 'text',
                        },
                        'all_meta': {
                            'type': 'text',
                        },
                    },
                },
            }

            self.client.indices.create(index=self.index, body=body)

    def status(self):
        return 'ok' if self.client.ping() else 'error'

    def get(self, ids):
        body = {'query': {'ids': {'values': ids}}}

        try:
            results = self.client.search(
                index=self.index, doc_type=self.type,
                body=body, size=len(ids),
            )

            for x in results['hits']['hits']:
                yield x['_source']
        except exceptions.NotFoundError:
            return []

    def insert(self, generator):
        def add_fields(generator):
            for x in generator:
                logger.info(f"Insert: {x['id']} into {self.index}")
                yield {'_id': x['id'], '_index': self.index, **x}

        bulk(client=self.client, actions=add_fields(generator))

    def delete(self, indices):
        for index in indices:
            try:
                self.client.indices.delete(index=index, ignore=[400])
            except exceptions.NotFoundError:
                return 'error'

        return 'ok'

    def search(self, body, limit=100, offset=0):
        try:
            results = self.client.search(
                index=self.index, doc_type=self.type,
                body=body, from_=offset, size=limit,
            )

            total = results['hits']['total']['value']
            hits = [x['_source'] for x in results['hits']['hits']]

            return {'total': total, 'entries': hits}
        except exceptions.NotFoundError:
            return {'total': 0, 'entries': []}

    def aggregate(self, body):
        try:
            results = self.client.search(
                index=self.index, doc_type=self.type,
                body=body, size=0,
            )

            return results['aggregations']
        except exceptions.NotFoundError:
            return []

    @staticmethod
    def build_body(query):
        terms = {'must': [], 'should': [], 'must_not': []}

        for x in query.get('text_search', []):
            term = None

            if x.get('field', 'all-text') == 'all-text':
                term = Q('multi_match', fields=['all_text'], query=x['query'])
            else:
                field_path = [y for y in x['field'].split('.') if y]

                if len(field_path) == 1:
                    if field_path[0] == 'meta':
                        term = Q('multi_match', fields=['all_meta'], query=x['query'])
                elif len(field_path) == 2:
                    if field_path[0] == 'meta':
                        term = Q('nested', path='meta', query=Q('bool', must=[
                            Q('match', meta__name=field_path[1]),
                            Q('match', meta__value_str=x['query']),
                        ]))
                    elif field_path[0] == 'tags':
                        term = Q('nested', path='tags', query=Q('bool', must=[
                            Q('match', tags__name=x['query']),
                            Q('range', tags__count={'gte': 2}),
                        ]))
                    elif field_path[0] == 'source':
                        term = Q('nested', path='source', query=Q('bool', must=[
                            Q('match', source__name=x['query']),
                        ]))

            if term is None:
                continue

            if x.get('flag'):
                if x['flag'] == 'must':
                    terms['must'].append(term)
                elif x['flag'] == 'should':
                    terms['should'].append(term)
                else:
                    terms['must_not'].append(term)
            else:
                terms['should'].append(term)

        for x in query.get('range_search', []):
            term = None

            if not x.get('field'):
                continue
            else:
                field_path = [y for y in x['field'].split('.') if y]

                if len(field_path) == 2:
                    if field_path[0] == 'meta':
                        if x['relation'] == 'eq':
                            value_match = Q('term', meta__value_int=x['query'])
                        else:
                            query = {x['relation']: x['query']}
                            value_match = Q('range', meta__value_int=query)

                        term = Q('nested', path='meta', query=Q('bool', must=[
                            Q('match', meta__name=field_path[1]),
                            value_match,
                        ]))

            if term is None:
                continue

            if x.get('flag'):
                if x['flag'] == 'must':
                    terms['must'].append(term)
                elif x['flag'] == 'should':
                    terms['should'].append(term)
                else:
                    terms['must_not'].append(term)
            else:
                terms['should'].append(term)

        if query.get('sorting'):
            if query['sorting'].lower() == 'random':
                seed = query.get('seed', uuid.uuid4().hex)
                functions = [{'random_score': {'seed': seed}}]

                terms['should'].append(Q('function_score', functions=functions))

        logger.info(f'[Server] Query {terms}')

        search = Search().query(
            Q(
                'bool',
                must=terms['must'],
                should=terms['should'],
                must_not=terms['must_not'],
            )
        )

        return search.to_dict()
