import logging

from opensearchpy.helpers import bulk
from opensearch_dsl import (
    connections,
    Search,
    Index,
    Q,
    A,
)
from .models import Resource

logger = logging.getLogger(__name__)


class Backbone:
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.host = config.get('host', 'opensearch')
        self.port = config.get('port', 9200)

        connections.create_connection(
            hosts=[f'{self.host}:{self.port}'],
            http_compress=True,
            ssl_show_warn=False,
            use_ssl=False,
            ssl_assert_hostname=False, 
        )

        self.client = connections.get_connection()
        self.index = config.get('index', 'artigo')

        index = Index(self.index)

        if not index.exists():
            index.aliases(default={})
            index.document(Resource)
            index.create()

    def status(self):
        return 'ok' if self.client.ping() else 'error'

    def get(self, ids):
        result = Resource.mget(ids, index=self.index)

        return self.convert(result)

    def insert(self, generator):
        def resources(generator):
            for x in generator:
                resource = Resource()
                resource.meta.id = x['id']

                if x.get('source'):
                    resource.add_collection(x['source'])

                if x.get('hash_id'):
                    resource.hash_id = x['hash_id']

                for meta in x.get('meta', []):
                    resource.add_metadata(meta)

                for tag in x.get('tags', []):
                    resource.add_tag(tag)

                result = resource.to_dict(True)
                    
                yield {'_index': self.index, **result}

        bulk(self.client, actions=resources(generator))

    def delete(self):
        index = Index(self.index)

        if index.exists():
            index.delete()

        return 'ok'

    def search(self, body, limit=100, offset=0):
        limit = min(limit, 10000)
        offset = min(offset, 10000 - limit)
        
        result = Search.from_dict(body) \
            .extra(from_=offset, size=limit) \
            .execute()

        return {
            'total': result.hits.total.value,
            'entries': self.convert(result.hits),
        }

    def aggregate(self, body, **kwargs):
        def traverse(tree):
            for k, values in tree.items():
                if k == 'buckets':
                    for v in values:
                        yield  {
                            'name': v['key'],
                            'value': v['doc_count'],
                        }
                elif isinstance(values, dict):
                    yield from traverse(values)

        results = []

        for field in kwargs.get('fields', []):
            field_path = [y for y in field.split('.', 1) if y]

            if field_path[0].startswith('meta'):
                field_path[0] = 'metadata'

            if kwargs.get('significant'):
                terms = 'significant_terms'
            else:
                terms = 'terms'

            search = Search.from_dict(body) \
                .extra(
                    from_=kwargs.get('offset', 0),
                    size=kwargs.get('limit', 0),
                )

            if len(field_path) == 1:
                search.aggs \
                    .bucket(
                        field_path[0],
                        'nested',
                        path=field_path[0],
                    ) \
                    .bucket(
                        f'{field_path[0]}_{terms}',
                        terms,
                        field=f'{field_path[0]}.name.keyword',
                        size=kwargs.get('size', 10),
                        min_doc_count=2,
                    )
            elif len(field_path) == 2:
                search.aggs \
                    .bucket(
                        field_path[0],
                        'nested',
                        path=field_path[0],
                    ) \
                    .bucket(
                        f'{field_path[0]}_filter',
                        A(
                            'filter',
                            filter=Q(
                                'term',
                                **{f'{field_path[0]}.name': field_path[1]},
                            )
                        )
                    ) \
                    .bucket(
                        f'{field_path[0]}_{terms}',
                        terms,
                        field=f'{field_path[0]}.value_str.keyword',
                        size=kwargs.get('size', 10),
                        min_doc_count=1,
                    )
            else:
                continue

            result = search.execute().to_dict()

            results.append({
                'field': field,
                'entries': list(traverse(result)),
            })

        return results

    @staticmethod
    def convert(hits):
        def loop(hits):
            for x in hits:
                result = x.to_dict()
                result['meta'] = x.meta.to_dict()

                yield result

        return list(loop(hits))
