import logging
import traceback

from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.models import Collection
from frontend.serializers import CollectionCountSerializer as Serializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class CollectionsView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = dict(request.query_params)

        try:
            params['limit'] = int(params['limit'][0])
        except:
            params['limit'] = 96

        try:
            params['offset'] = int(params['offset'][0])
        except:
            params['offset'] = 0

        collections = Collection.objects.filter(user=request.user)

        if params.get('query'):
            if not isinstance(params['query'], (list, set)):
                params['query'] = [params['query']]

            query = Q()

            for name in params['query']:
                query |= Q(name__icontains=name)

            collections = collections.filter(query)

        collections = collections.annotate(
                resource_ids=ArrayAgg('resources__id'),
            ) \
            .order_by('-created') \
            .values(
                'hash_id',
                'name',
                'status',
                'progress',
                'created',
                'resource_ids',
            )

        result = {'total': len(collections)}

        limit = params['offset'] + params['limit']
        collections = collections[params['offset']:limit]
        collections = Serializer(collections, many=True).data

        result['offset'] = params['offset']
        result['entries'] = collections

        return Response(result)
