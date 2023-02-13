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
    UserROI,
    UserTagging,
)
from frontend.serializers import SessionCountSerializer as Serializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['POST'], exclude=True)
class SessionsView(APIView):
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

        gamerounds = Gameround.objects.filter(user=request.user)

        if params.get('query'):
            gameround_ids = set()

            if params['query'].get('all-text'):
                tag_name = params['query']['all-text']

                for model in (UserROI, UserTagging):
                    ids = model.objects.filter(user=request.user) \
                        .filter(tag__name__icontains=tag_name) \
                        .values_list('gameround_id', flat=True)

                    gameround_ids.update(ids)
            elif params['query'].get('hide-empty'):
                for model in (UserROI, UserTagging):
                    ids = model.objects.filter(user=request.user) \
                        .values_list('gameround_id', flat=True)

                    gameround_ids.update(ids)

            if gameround_ids:
                gamerounds = gamerounds.filter(id__in=gameround_ids)

        gamerounds = gamerounds.values('gamesession') \
            .annotate(
                rois=Coalesce(Count('userrois'), 0),
                taggings=Coalesce(Count('usertaggings'), 0),
                resource_ids=ArrayAgg('resource_id'),
            ) \
            .annotate(annotations=F('rois') + F('taggings')) \
            .order_by('-gamesession__created') \
            .values(
                'gamesession_id',
                'gamesession__created',
                'resource_ids',
                'annotations',
            )

        result = {
            'total': len(gamerounds),
            'offset': params['offset'],
        }

        gamerounds = gamerounds[params['offset']:params['limit']]
        result['entries'] = Serializer(gamerounds, many=True).data

        return Response(result)
