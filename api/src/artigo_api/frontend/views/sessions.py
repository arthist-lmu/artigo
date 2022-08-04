import logging
import traceback

from django.db.models import Count, F
from django.db.models.functions import Coalesce
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.models import (
    Gameround,
    UserTagging,
)
from frontend.serializers import SessionCountSerializer as Serializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class SessionsView(APIView):
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

        gamerounds = Gameround.objects.filter(user=request.user)

        if params.get('query'):
            gameround_ids = UserTagging.objects \
                .filter(tag__name__in=params['query']) \
                .values_list('gameround_id', flat=True)

            gamerounds = gamerounds.filter(id__in=gameround_ids)

        gamerounds = gamerounds.values('gamesession') \
            .annotate(
                rois=Coalesce(Count('userrois'), 0),
                taggings=Coalesce(Count('usertaggings'), 0),
                resources=ArrayAgg('resource__hash_id'),
            ) \
            .annotate(annotations=F('rois') + F('taggings')) \
            .order_by('-gamesession__created') \
            .values(
                'gamesession_id',
                'gamesession__created',
                'resources',
                'annotations',
            )

        result = {'total': len(gamerounds)}

        limit = params['offset'] + params['limit']
        gamerounds = gamerounds[params['offset']:limit]
        gamerounds = Serializer(gamerounds, many=True).data

        result['offset'] = params['offset']
        result['entries'] = gamerounds

        return Response(result)
