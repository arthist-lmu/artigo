import logging

from opensearchpy import OpenSearch
from opensearch_dsl import Q

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, backbone):
        self.backbone = backbone

    def __call__(self, query, fields, size=250):
        aggregations = []

        for field in fields:
            field_path = [y for y in field.split('.') if y]
            body = self.build_body(query, *field_path, size=size)

            aggregations.append({
                'field': field,
                'entries': self.backbone.aggregate(body),
            })

        return aggregations

    @staticmethod
    def build_body(query, field, subfield=None, size=5):
        value = 'name' if subfield is None else 'value_str'

        aggs = {
            'aggs': {
                f'{field}_aggr': {
                    'terms': {
                        'size': size,
                        'field': f'{field}.{value}.keyword',
                    },
                },
            },
        }

        if subfield is not None:
            aggs = {
                'aggs': {
                    f'{field}_filter': {
                        'filter': {
                            'term': {
                                f'{field}.name': subfield,
                            },
                        },
                        **aggs,
                    },
                },
            }

        body = {
            'aggs': {
                f'{field}': {
                    'nested': {
                        'path': field,
                    },
                    **aggs,
                },
            },
        }

        if query is not None:
            body['query'] = query

        return body
