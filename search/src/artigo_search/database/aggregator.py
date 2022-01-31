import logging

from opensearchpy import OpenSearch
from opensearch_dsl import Q


class Aggregator:
    def __init__(self, backbone):
        self.backbone = backbone

    def __call__(self, query, fields, size=250):
        aggregations = []

        for field in fields:
            field_path = [y for y in x['field'].split('.') if y]

            if field_path[0] not in ['meta', 'tags']:
                continue

            if len(field_path) == 1:
                body = self.build_body(query, field_path[0], size=size)
                entries = list(self.get_entries(body, field_path[0]))
            elif len(field_path) == 2:
                body = self.build_body(query, *field_path, size=size)
                entries = list(self.get_entries(body, field_path[0]))
            else:
                continue

            if entries and len(entries) > 0:
                aggregations.append({'field': field, 'entries': entries})

        return aggregations

    def get_entries(self, body, nested_field):
        results = self.backbone.aggregate(body)[f'{nested_field}_nested']

        if results.get(f'{nested_field}_name_filter'):
            results = results[f'{nested_field}_name_filter']

        for x in results[f'{nested_field}_name_filter_aggr']['buckets']:
            yield {'name': x['key'], 'value': x['doc_count']}

    @staticmethod
    def build_body(query, nested_field, field=None, size=5):
        # TODO: transform to DSL

        if field is not None:
            body = {
                'aggs': {
                    f'{nested_field}_nested': {
                        'nested': {
                            'path': f'{nested_field}',
                        },
                        'aggs': {
                            f'{nested_field}_name_filter': {
                                'filter': {
                                    'term': {
                                        f'{nested_field}.name': field,
                                    },
                                },
                                'aggs': {
                                    f'{nested_field}_name_filter_aggr': {
                                        'terms': {
                                            'size': size,
                                            'field': f'{nested_field}.value_str.keyword',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            }
        else:
            body = {
                'aggs': {
                    f'{nested_field}_nested': {
                        'nested': {
                            'path': f'{nested_field}',
                        },
                        'aggs': {
                            f'{nested_field}_name_filter_aggr': {
                                'terms': {
                                    'size': size,
                                    'field': f'{nested_field}.value_str.keyword',
                                },
                            },
                        },
                    },
                },
            }

        if query is not None:
            body['query'] = query

        return body
