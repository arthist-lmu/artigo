import grpc
import logging
import traceback

from frontend.utils import media_url_to_image
from frontend.utils import RetryOnRpcErrorClientInterceptor, ExponentialBackoff
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

#from artigo_search import index_pb2, index_pb2_grpc
#from artigo_search.utils import meta_from_proto

logger = logging.getLogger(__name__)


class SearchView(APIView):
    def parse_request(params):
        grpc_request = index_pb2.SearchRequest()

        if params.get('query'):
            for query in params['query']:
                term = grpc_request.terms.add()
                term.text.field = 'all'
                term.text.query = query['value']

                if query.get('flag') == 'must':
                    term.text.flag = index_pb2.TextSearchTerm.MUST
                elif query.get('flag') == 'not':
                    term.text.flag = index_pb2.TextSearchTerm.NOT
                else:
                    term.text.flag = index_pb2.TextSearchTerm.SHOULD

        if params.get('time_span'):
            time_span = params['time_span']

            if not isinstance(time_span, (list, set)):
                time_span = [time_span]

            if len(time_span) > 1:
                term = grpc_request.terms.add()
                term.number.field = 'meta.year_max'
                term.number.int_query = max(time_span)
                term.number.flag = index_pb2.NumberSearchTerm.MUST
                term.number.relation = index_pb2.NumberSearchTerm.LESS_EQ

            term = grpc_request.terms.add()
            term.number.field = 'meta.year_min'
            term.number.int_query = min(time_span)
            term.number.flag = index_pb2.NumberSearchTerm.MUST
            term.number.relation = index_pb2.NumberSearchTerm.GREATER_EQ

        if params.get('aggregate'):
            for field in params['aggregate']:
                grpc_request.aggregate.fields.extend([field])
                grpc_request.aggregate.size = 250

        return grpc_request

    def rpc_check_search(job_id):
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
            entries, aggregate = [], []

            for x in response.entries:
                entries.append({
                    'id': x.id,
                    'meta': meta_from_proto(x.meta),
                    'path': media_url_to_image(x.id),
                })

            for x in response.aggregate:
                values = {'field': x.field, 'entries': []}

                for entry in x.entries:
                    values['entries'].append({
                        'name': entry.key,
                        'count': entry.int_val,
                    })

                aggregate.append(values)

            return {'entries': entries, 'aggregate': aggregate, 'state': 'done'}
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.FAILED_PRECONDITION:
                return {'job_id': job_id, 'state': 'pending'}

        raise APIException()

    def rpc_search(params):
        grpc_request = self.parse_request(params)

        grpc_request_bin = grpc_request.SerializeToString()
        grpc_request_hash = hashlib.sha256(grpc_request_bin).hexdigest()

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

        return {'job_id': response.id, 'state': 'pending'}

    def get(self, request, format=None):
        job_id = request.query_params.get('job_id')

        if job_id:
            result = self.rpc_check_search(job_id)
        else:
            result = self.rpc_search(request.query_params)

        return Response(result)
