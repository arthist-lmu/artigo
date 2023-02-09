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
    Resource,
    Gamesession,
    Gameround,
    UserROI,
    UserTagging,
)
from frontend.serializers import (
    SessionSerializer,
    ResourceSerializer,
)
from .utils import ResourceViewHelper

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class SessionView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.query_params

        if not params.get('id'):
            raise ParseError('session_id_is_required')

        try:
            gamesession = Gamesession.objects.get(id=params['id'])
        except Gamesession.DoesNotExist:
            raise NotFound('gamesession_is_unknown')

        if gamesession.game_type.name.lower() == 'tagging':
            taggings = UserTagging.objects
        elif gamesession.game_type.name.lower() == 'roi':
            taggings = UserROI.objects
        else:
            raise ParseError('game_type_is_not_implemented')

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
        taggings = SessionSerializer(
            taggings,
            many=True,
            context={'ids': resource_ids},
        ).data

        for tagging in taggings:
            resource_id = str(tagging['resource_id'])
            
            if session.get(resource_id):
                session[resource_id].update(tagging)
            else:
                resource = Resource.objects.get(id=resource_id)
                resource = ResourceSerializer(resource).data

                session[resource_id] = tagging
                session[resource_id]['meta'] = []
                session[resource_id]['path'] = resource['path']

                for key, values in resource.items():
                    if isinstance(values, (list, set)):
                        for value in values:
                            session[resource_id]['meta'].append({
                                'name': key,
                                'value_str': value['name'],
                            })
                    else:
                        if not isinstance(values, dict):
                            values = { 'name': values }

                        session[resource_id]['meta'].append({
                            'name': key,
                            'value_str': values['name'],
                        })

        return Response(session.values())


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
