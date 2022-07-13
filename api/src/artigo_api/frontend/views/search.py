import grpc
import hashlib
import msgpack
import logging

from collections import defaultdict
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.utils import media_url_to_image, channel
from .utils import RPCView

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto, tags_from_proto

logger = logging.getLogger(__name__)

MAPPER = {
    'tags': 'tags',
    'source': 'collection',
    '': 'all-text',
    'all-text': 'all-text',
}


class SearchView(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.SearchRequest()

        if params.get('query'):
            query = params['query']

            if isinstance(query, str):
                query = {'all-text': query}
            elif isinstance(query, list):
                query_dict = defaultdict(list)

                for q in query:
                    if not isinstance(q, dict):
                        q = {'value': q}

                    field = q.get('name', 'all-text')
                    query_dict[field].append(q)

                query = query_dict

            if isinstance(query, dict):
                for field, queries in query.items():
                    if isinstance(queries, str):
                        queries = queries.split()
                    elif not isinstance(queries, (set, list)):
                        queries = [queries]

                    for q in queries:
                        term = grpc_request.terms.add()

                        if not isinstance(q, dict):
                            q = {'value': q}

                        if q.get('value'):
                            if q['value'].startswith('+'):
                                q['flag'] = 'must'
                                q['value'] = q['value'][1:]
                            elif q['value'].startswith('-'):
                                q['flag'] = 'not'
                                q['value'] = q['value'][1:]

                            term.text.query = q['value']

                        if MAPPER.get(field):
                            term.text.field = MAPPER[field]
                        else:
                            term.text.field = f'meta.{field}'

                        if q.get('flag') == 'should':
                            term.text.flag = index_pb2.TextSearchTerm.SHOULD
                        elif q.get('flag') == 'not':
                            term.text.flag = index_pb2.TextSearchTerm.NOT
                        else:
                            term.text.flag = index_pb2.TextSearchTerm.MUST

        if params.get('date_range'):
            date_range = params['date_range']

            if not isinstance(date_range, (list, set)):
                date_range = [date_range]

            if len(date_range) > 1:
                term = grpc_request.terms.add()
                term.number.field = 'meta.year_max'
                term.number.int_query = max(date_range)
                term.number.flag = indexer_pb2.NumberSearchTerm.MUST
                term.number.relation = indexer_pb2.NumberSearchTerm.LESS_EQ

            term = grpc_request.terms.add()
            term.number.field = 'meta.year_min'
            term.number.int_query = min(date_range)
            term.number.flag = indexer_pb2.NumberSearchTerm.MUST
            term.number.relation = indexer_pb2.NumberSearchTerm.GREATER_EQ

        if params.get('aggregate'):
            aggregate = params['aggregate']

            for field in aggregate.get('fields', []):
                grpc_request.aggregate.fields.extend([field])

            if isinstance(aggregate.get('size'), int):
                grpc_request.aggregate.size = aggregate['size']
            else:
                grpc_request.aggregate.size = 250

            grpc_request.aggregate.use_query = aggregate.get('use_query', True)
            grpc_request.aggregate.significant = aggregate.get('significant', False)

        if params.get('random'):
            grpc_request.sorting = index_pb2.SearchRequest.SORTING_RANDOM

            if isinstance(params['random'], (int, float, str)):
                grpc_request.seed = str(params['random'])

        if isinstance(params.get('limit'), int):
            grpc_request.limit = params['limit']
        else:
            grpc_request.limit = 100

        if isinstance(params.get('offset'), int):
            grpc_request.offset = params['offset']
        else:
            grpc_request.offset = 0

        return grpc_request

    def rpc_check_post(self, job_id):
        grpc_request = index_pb2.ListSearchResultRequest(id=job_id)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.list_search_result(grpc_request)

            entries = []

            for x in response.entries:
                entry = {
                    'resource_id': x.id,
                    'meta': meta_from_proto(x.meta),
                    'tags': tags_from_proto(x.tags),
                }

                if x.hash_id:
                    entry['path'] = media_url_to_image(x.hash_id)

                if x.source.id:
                    entry['source'] = {
                        'id': x.source.id,
                        'name': x.source.name,
                        'url': x.source.url,
                        'is_public': x.source.is_public,
                    }

                entries.append(entry)

            aggregations = []

            for x in response.aggregations:
                values = {
                    'field': x.field,
                    'entries': [],
                }

                for entry in x.entries:
                    values['entries'].append({
                        'name': entry.key,
                        'count': entry.int_val,
                    })

                aggregations.append(values)

            return {
                'total': response.total,
                'offset': response.offset,
                'entries': entries,
                'aggregations': aggregations,
            }
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.FAILED_PRECONDITION:
                return {'job_id': job_id}

    def rpc_post(self, params):
        grpc_request = self.parse_request(params)

        grpc_request_bin = grpc_request.SerializeToString()
        grpc_request_hash = hashlib.sha256(grpc_request_bin).hexdigest()

        response_cache = cache.get(grpc_request_hash)

        if response_cache is not None:
            return msgpack.unpackb(response_cache)

        stub = index_pb2_grpc.IndexStub(self.channel)
        response = stub.search(grpc_request)

        cache.set(response.id, grpc_request_hash)

        return {'job_id': response.id}

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='query',
                type={
                    'type': 'array',
                    'items': {
                        'properties': {
                            'name': {
                                'description': 'Name of field',
                                'type': 'string',
                                'enum': [
                                    'titles',
                                    'creators',
                                    'location',
                                    'institution',
                                    'source',
                                    'tags',
                                    'all-text',
                                ],
                            },
                            'value': {
                                'description': 'Value of field',
                                'type': 'string',
                            },
                            'flag': {
                                'description': 'For more information, see the [OpenSearch Documentation]' \
                                    + '(https://opensearch.org/docs/latest/opensearch/query-dsl/bool/)',
                                'type': 'string',
                                'enum': [
                                    'should',
                                    'must',
                                    'not',
                                ],
                            },
                        },
                    }
                },
            ),
            OpenApiParameter(
                description='Aggregation options',
                name='aggregate',
                type={
                    'type': 'object',
                    'properties': {
                        'fields': {
                            'description': 'Metadata fields that should be aggregated',
                            'type': 'array',
                        },
                        'size': {
                            'description': 'Maximum number of aggregation results',
                            'type': 'integer',
                            'default': 250,
                        },
                    },
                },
            ),
            OpenApiParameter(
                description='Random seed',
                name='random',
                type=str,
            ),
            OpenApiParameter(
                description='Maximum number of search results',
                name='limit',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 10000,
                },
                default=100,
            ),
            OpenApiParameter(
                description='Number of search results to skip',
                name='offset',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 10000,
                },
                default=0,
            ),
            OpenApiParameter(
                description='Receive status updates of the respective job',
                name='job_id',
                type=str,
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total': {
                        'type': 'integer',
                    },
                    'offset': {
                        'type': 'integer',
                    },
                    'entries': {
                        'type': 'array',
                        'items': {
                            'properties': {
                                'id': {
                                    'type': 'string',
                                },
                                'meta': {
                                    'type': 'array',
                                    'items': {
                                        'properties': {
                                            'name': {
                                                'type': 'string',
                                            },
                                            'value_str': {
                                                'type': 'string',
                                            },
                                        },
                                    },
                                },
                                'tags': {
                                    'type': 'array',
                                    'items': {
                                        'properties': {
                                            'id': {
                                                'type': 'string',
                                            },
                                            'name': {
                                                'type': 'string',
                                            },
                                            'language': {
                                                'type': 'string',
                                            },
                                            'count': {
                                                'type': 'integer',
                                            },
                                        },
                                    },
                                },
                                'path': {
                                    'type': 'string',
                                },
                                'source': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {
                                            'type': 'string',
                                        },
                                        'name': {
                                            'type': 'string',
                                        },
                                        'url': {
                                            'type': 'string',
                                        },
                                        'is_public': {
                                            'type': 'boolean',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'aggregations': {
                        'type': 'array',
                        'items': {
                            'properties': {
                                'field': {
                                    'type': 'string',
                                },
                                'entries': {
                                    'type': 'array',
                                    'items': {
                                        'properties': {
                                            'name': {
                                                'type': 'string',
                                            },
                                            'count': {
                                                'type': 'integer',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        description='Search metadata and crowd-generated tags of resources.' \
            + ' For longer lasting queries a `job_id` is returned, which can' \
            + ' be used in subsequent queries to receive status updates.',
    )
    def post(self, request, format=None):
        if request.data.get('params'):
            params = request.data['params']
        else:
            params = request.query_params

        job_id = params.get('job_id')

        if job_id:
            result = self.rpc_check_post(job_id)
        else:
            result = self.rpc_post(params)

        if result is None:
            raise APIException('unknown_error')

        return Response(result)
