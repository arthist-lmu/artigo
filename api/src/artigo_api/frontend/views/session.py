import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ParseError,
    NotFound,
)
from drf_spectacular.utils import extend_schema
from frontend.models import (
    Gamesession,
    Gameround,
    UserROI,
    UserTagging,
)
from frontend.serializers import SessionSerializer as Serializer
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

        try:
            gamesession = Gamesession.objects.get(id=params['id'])
        except Gamesession.DoesNotExist:
            raise NotFound('unknown_gamesession')

        # if gamesession.user != request.user:
        #     raise ParseError('user_access_denied')

        if gamesession.game_type.name == 'tagging':
            taggings = UserTagging.objects
        elif gamesession.game_type.name == 'roi':
            taggings = UserROI.objects
        else:
            raise ParseError('game_type_not_implemented')

        gamerounds = Gameround.objects.filter(gamesession=gamesession)
        resource_ids = gamerounds.values_list('resource_id', flat=True)

        taggings = taggings.filter(gameround__in=gamerounds) \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
                'score',
            )

        session = ResourceView()(resource_ids)

        for tagging in Serializer(taggings, many=True).data:
            session[str(tagging['resource_id'])].update(tagging)

        return Response(session.values())


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
