import logging
import traceback

from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ParseError,
    NotFound,
)
from drf_spectacular.utils import extend_schema
from frontend.models import Gameround, Tagging
from frontend.serializers import SessionSerializer
from .utils import ResourceViewHelper

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class SessionView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.query_params

        if not params.get('id'):
            raise ParseError('session_id_required')

        gamerounds = Gameround.objects.filter(
                gamesession_id=params['id'],
                user=request.user,
            )

        if gamerounds.count() == 0:
            raise NotFound('unknown_gamesession')

        taggings = Tagging.objects.filter(gameround__in=gamerounds) \
            .values('resource') \
            .annotate(
                count_tags=Count('tag'),
                sum_score=Sum('score'),
            ) \
            .values(
                'resource_id',
                'count_tags',
                'sum_score',
            )

        resource_ids = gamerounds.values_list('resource_id', flat=True)
        session = ResourceView()(resource_ids)

        for x in SessionSerializer(taggings, many=True).data:
            session[str(x['resource_id'])].update(x)

        return Response(session.values())


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
