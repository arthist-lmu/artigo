import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.controllers import (
    game_controller_switch,
    input_controller_switch,
)

logger = logging.getLogger(__name__)


class GameView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                description='Type of game',
                name='game_type',
                type=str,
                enum=[
                    'tagging',
                    'roi',
                ],
                default='tagging',
            ),
            OpenApiParameter(
                description='Duration of each gameround (in seconds).' \
                    + ' For infinite game rounds, `0` should be passed.',
                name='game_round_duration',
                type={
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 60 * 60,
                },
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
                description='Number of resources. This corresponds to the' \
                    + ' number of gamerounds to be played.',
                name='resource_rounds',
                type={
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 100,
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
                description='Suggester type',
                name='suggester_type',
                type={
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'enum': [
                            'cooccurrence_suggester',
                        ],
                    },
                },
            ),
            OpenApiParameter(
                description='Score type',
                name='score_type',
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
        description='Create games. The first valid game round is automatically' \
            + ' returned when a new game is created. All further rounds can be' \
            + ' obtained by passing the respective `session_id`.',
    )
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        result = game_controller_switch(request)

        if result.get('type', 'error') == 'error':
            message = result.get('message', 'unknown_error')

            raise APIException(message)

        return Response(result)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        result = input_controller_switch(request)

        if result.get('type', 'error') == 'error':
            message = result.get('message', 'unknown_error')

            raise APIException(message)

        return Response(result)
