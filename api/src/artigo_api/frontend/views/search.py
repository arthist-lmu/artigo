import grpc
import hashlib
import msgpack
import logging
import traceback

from .utils import RPCView
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.utils import media_url_to_image

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto, tags_from_proto

logger = logging.getLogger(__name__)


class Search(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.SearchRequest()

        if params.get('query'):
            query = params['query']

            if not isinstance(query, dict):
                query = {'all-text': query}

            for field, queries in query.items():
                if isinstance(queries, str):
                    queries = queries.split()
                elif not isinstance(queries, (set, list)):
                    queries = [queries]

                for query in queries:
                    if not isinstance(query, dict):
                        query = {'value': query}

                    if query['value'].startswith('+'):
                        query['flag'] = 'must'
                        query['value'] = query['value'][1:]
                    elif query['value'].startswith('-'):
                        query['flag'] = 'not'
                        query['value'] = query['value'][1:]

                    term = grpc_request.terms.add()
                    term.text.query = query['value']

                    if field == 'tags':
                        term.text.field = 'tags.name'
                    elif field == 'source':
                        term.text.field = 'source.name'
                    elif field in ['all-text', '']:
                        term.text.field = 'all-text'
                    else:
                        term.text.field = f'meta.{field}'

                    if query.get('flag') == 'must':
                        term.text.flag = index_pb2.TextSearchTerm.MUST
                    elif query.get('flag') == 'not':
                        term.text.flag = index_pb2.TextSearchTerm.NOT
                    else:
                        term.text.flag = index_pb2.TextSearchTerm.SHOULD

        for field in params.get('aggregate', []):
            grpc_request.aggregate.fields.extend([field])
            grpc_request.aggregate.size = 250

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
        stub = index_pb2_grpc.IndexStub(self.channel)
        request = index_pb2.ListSearchResultRequest(id=job_id)

        try:
            response = stub.list_search_result(request)

            entries = []

            for x in response.entries:
                entries.append({
                    'id': x.id,
                    'meta': meta_from_proto(x.meta),
                    'tags': tags_from_proto(x.tags),
                    'path': media_url_to_image(x.id),
                    'source': {
                        'id': x.source.id,
                        'name': x.source.name,
                        'url': x.source.url,
                        'is_public': x.source.is_public,
                    },
                })

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

        # if response_cache is not None:
        #     return msgpack.unpackb(response_cache)

        stub = index_pb2_grpc.IndexStub(self.channel)
        response = stub.search(grpc_request)

        cache.set(response.id, grpc_request_hash)

        return {'job_id': response.id}

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='query',
                type={
                    'type': 'object',
                    'properties': {
                        'titles': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                        'creators': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                        'location': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                        'institution': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                        'source': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                        'tags': {
                            'type': 'array',
                            'items': {
                                'properties': {
                                    'value': {
                                        'type': 'string',
                                    },
                                    'flag': {
                                        'type': 'string',
                                        'enum': [
                                            'should',
                                            'must',
                                            'not',
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
            ),
            OpenApiParameter(
                name='aggregate',
                type={
                    'type': 'array',
                    'items': {
                        'type': 'string',
                    },
                },
            ),
            OpenApiParameter(
                name='random',
                type=str,
            ),
            OpenApiParameter(
                name='limit',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 10000,
                },
            ),
            OpenApiParameter(
                name='offset',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 10000,
                },
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
        description='Search metadata and crowd-generated tags of resources.',
    )
    def post(self, request, format=None):
        job_id = request.data['params'].get('job_id')

        if job_id:
            result = self.rpc_check_post(job_id)
        else:
            result = self.rpc_post(request.data['params'])

        if result is None:
            raise APIException('unknown_error')

        return Response(result)
