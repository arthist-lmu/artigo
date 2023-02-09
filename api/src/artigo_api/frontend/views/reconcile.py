import grpc
import logging
import traceback

from .utils import RPCView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.models import Creator, Resource

from artigo_search import index_pb2, index_pb2_grpc

logger = logging.getLogger(__name__)


@extend_schema(methods=['POST'], exclude=True)
class ReconcileView(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.ReconcileRequest()

        if params.get('queries'):
            queries = params['queries']

            if not isinstance(queries, (set, list)):
                queries = [queries]

            for query in queries:
                if not isinstance(query, dict):
                    query = {'name': query}

                term = grpc_request.terms.add()
                term.name = query['name']

                if query.get('id'):
                    term.id = query['id']

                if query.get('type'):
                    term.type = query['type']

        if isinstance(params.get('size'), int):
            grpc_request.size = params['size']
        else:
            grpc_request.size = 5

        if params.get('lang'):
            grpc_request.lang = params['lang']

        return grpc_request

    def rpc_post(self, params):
        grpc_request = self.parse_request(params)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.reconcile(grpc_request)

            reconciliations = []

            for x in response.reconciliations:
                values = {
                    'name': x.term.name,
                    'type': x.term.type,
                    'service': x.service,
                    'entries': [],
                }

                if x.term.ids:
                    values['ids'] = set(x.term.ids)

                for entry in x.entries:
                    values['entries'].append({
                        'id': entry.id,
                        'name': entry.name,
                        'description': entry.description,
                        'score': entry.score,
                    })

                reconciliations.append(values)

            return {'reconciliations': reconciliations}
        except grpc.RpcError as error:
            logger.error(error)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        result = self.rpc_post(request.data['params'])

        if result is None:
            raise APIException('unknown_error')
        
        return Response(result)


@extend_schema(methods=['POST'], exclude=True)
class ReconcileAddView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.data['params']

        try:
            if params.get('type') == 'creator':
                if params.get('service') == 'Wikidata':
                    creator_ids = Resource.objects \
                        .filter(id__in=params['ids']) \
                        .values('creators__id')

                    Creator.objects.filter(id__in=creator_ids) \
                        .update(wikidata_id=params['entry_id'])
            elif params.get('type') == 'resource':
                if params.get('service') == 'Wikidata':
                    Resource.objects.filter(id__in=params['ids']) \
                        .update(wikidata_id=params['entry_id'])
        except Exception as error:
            raise APIException('unknown_error')

        return Response()


@extend_schema(methods=['POST'], exclude=True)
class ReconcileRemoveView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.data['params']

        try:
            if params.get('type') == 'creator':
                if params.get('service') == 'Wikidata':
                    creator_ids = Resource.objects \
                        .filter(id__in=params['ids']) \
                        .values('creators__id')

                    Creator.objects.filter(id__in=creator_ids) \
                        .update(wikidata_id='')
            elif params.get('type') == 'resource':
                if params.get('service') == 'Wikidata':
                    Resource.objects.filter(id__in=params['ids']) \
                        .update(wikidata_id='')
        except Exception as error:
            raise APIException('unknown_error')

        return Response()
