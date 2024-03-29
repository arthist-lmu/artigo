import json
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


@extend_schema(methods=['POST'], exclude=True)
class CollectionsView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        if request.data.get('params'):
            params = request.data['params']
        else:
            params = request.query_params

        if not isinstance(params.get('limit'), int):
            params['limit'] = 96

        if not isinstance(params.get('offset'), int):
            params['offset'] = 0

        params['limit'] += params['offset']

        filter_users = Q(user=request.user)

        if request.user.is_staff:
            filter_users |= Q(access__in=('O', 'P'))

        collections = Collection.objects.filter(filter_users) \
            .annotate(
                count_resources=Coalesce(Count('resources__id'), 0),
                resource_ids=ArrayAgg('resources__id'),
            )

        if params.get('query'):
            if params['query'].get('all-text'):
                name = params['query']['all-text'].strip()
                collections = collections.filter(titles__name__icontains=name)
            elif params['query'].get('hide-empty'):
                collections = collections.filter(count_resources__gt=0)

        collections = collections.order_by('-created')

        result = {
            'total': len(collections),
            'offset': params['offset'],
        }

        collections = collections[params['offset']:params['limit']]
        result['entries'] = Serializer(collections, many=True).data

        return Response(result)
