import json
import logging
import traceback

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.controllers import GameController, TagController

logger = logging.getLogger(__name__)


class GameView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                description='Number of gamerounds',
                name='rounds',
                type={
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 100,
                },
                default=5,
            ),
            OpenApiParameter(
                description='Duration of each gameround (in seconds).' \
                    + ' For infinite game rounds, `0` should be passed.',
                name='round_duration',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 60 * 60,
                },
                default=60,
            ),
            OpenApiParameter(
                description='Type of each resource',
                name='resource_type',
                type=str,
                enum=[
                    'random_resource',
                ],
            ),
            OpenApiParameter(
                description='Resource options',
                name='resource_options',
                type={
                    'type': 'object',
                    'properties': {
                        'lt_percentile': {
                            'type': 'number',
                            'default': 1.0,
                        },
                    },
                },
            ),
            OpenApiParameter(
                description='Type of each opponent. Opponents are invalid' \
                    + ' for infinite game rounds (`round_duration=0`).',
                name='opponent_type',
                type=str,
                enum=[
                    'mean_gameround_opponent',
                    'random_gameround_opponent',
                ],
            ),
            OpenApiParameter(
                description='Type of taboo annotations',
                name='taboo_type',
                type=str,
                enum=[
                    'most_annotated_taboo',
                ],
            ),
            OpenApiParameter(
                description='Score types',
                name='score_types',
                type={
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'enum': [
                            'annotation_validated_score',
                            'opponent_validated_score',
                        ],
                    },
                },
            ),
        ],
    )
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        plugins = cache.get('plugins', {})

        game_controller = GameController(
            resource_plugin_manager=plugins.get('resource'),
            opponent_plugin_manager=plugins.get('opponent'),
            taboo_plugin_manager=plugins.get('taboo'),
        )

        result = game_controller(request.query_params, request.user)

        if result.get('type', 'error') == 'error':
            message = result.get('message', 'unknown_error')

            raise APIException(message)

        return Response(result)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        plugins = cache.get('plugins', {})

        tag_controller = TagController(
            score_plugin_manager=plugins.get('score'),
        )

        result = tag_controller(request.data['params'], request.user)

        if result.get('type', 'error') == 'error':
            message = result.get('message', 'unknown_error')

            raise APIException(message)

        return Response(result)
