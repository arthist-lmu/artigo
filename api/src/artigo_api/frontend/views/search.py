import grpc
import hashlib
import msgpack
import logging
import traceback

from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from frontend.utils import media_url_to_image
from frontend.utils import RetryOnRpcErrorClientInterceptor, ExponentialBackoff

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto, tags_from_proto

logger = logging.getLogger(__name__)


class SearchView(APIView):
    def parse_request(self, params):
        grpc_request = index_pb2.SearchRequest()

        if params.get('query'):
            if not isinstance(params['query'], dict):
                params['query'] = {'': params['query']}

            for field, queries in params['query'].items():
                if isinstance(queries, str):
                    queries = queries.split()
                elif not isinstance(queries, (set, list)):
                    queries = [queries]

                for query in queries:
                    if not isinstance(query, dict):
                        query = {'value': query}

                    term = grpc_request.terms.add()
                    term.text.query = query['value']

                    if field == 'tags':
                        term.text.field = 'tags.name'
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

        if params.get('random') and isinstance(params['random'], (int, float, str)):
            grpc_request.sorting = index_pb2.SearchRequest.SORTING_RANDOM
            grpc_request.seed = str(params['random'])

        return grpc_request

    def rpc_check_search(self, job_id):
        interceptors = (
            RetryOnRpcErrorClientInterceptor(
                max_attempts=4,
                sleeping_policy=ExponentialBackoff(
                    init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
                ),
                status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
            ),
        )

        channel = grpc.intercept_channel(
            grpc.insecure_channel(
                f'{settings.GRPC_HOST}:{settings.GRPC_PORT}',
                options=[
                    ('grpc.max_send_message_length', 50 * 1024 * 1024),
                    ('grpc.max_receive_message_length', 50 * 1024 * 1024),
                ],
            ),
            *interceptors,
        )

        stub = index_pb2_grpc.IndexStub(channel)
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
                })

            aggregations = []

            for x in response.aggregations:
                values = {'field': x.field, 'entries': []}

                for entry in x.entries:
                    values['entries'].append({
                        'name': entry.key,
                        'count': entry.int_val,
                    })

                aggregations.append(values)

            return {'entries': entries, 'aggregations': aggregations}
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.FAILED_PRECONDITION:
                return {'job_id': job_id}


    def rpc_search(self, params):
        grpc_request = self.parse_request(params)

        grpc_request_bin = grpc_request.SerializeToString()
        grpc_request_hash = hashlib.sha256(grpc_request_bin).hexdigest()

        response_cache = cache.get(grpc_request_hash)

        # if response_cache is not None:
        #     return msgpack.unpackb(response_cache)

        interceptors = (
            RetryOnRpcErrorClientInterceptor(
                max_attempts=4,
                sleeping_policy=ExponentialBackoff(
                    init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
                ),
                status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
            ),
        )

        channel = grpc.intercept_channel(
            grpc.insecure_channel(
                f'{settings.GRPC_HOST}:{settings.GRPC_PORT}',
                options=[
                    ('grpc.max_send_message_length', 50 * 1024 * 1024),
                    ('grpc.max_receive_message_length', 50 * 1024 * 1024),
                ],
            ),
            *interceptors,
        )

        stub = index_pb2_grpc.IndexStub(channel)
        response = stub.search(grpc_request)

        cache.set(response.id, grpc_request_hash)

        return {'job_id': response.id}

    def post(self, request, format=None):
        job_id = request.data['params'].get('job_id')

        if job_id:
            result = self.rpc_check_search(job_id)
        else:
            result = self.rpc_search(request.data['params'])

        if result is None:
            raise APIException('Search could not be executed.')

        return Response(result)
