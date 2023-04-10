import random
import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from frontend import cache

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class HomeView(APIView):
    def get(self, request, format=None):
        lang = request.query_params.get('lang', 'de')

        games = [
        	*cache.random_game_parameters(lang=lang),
        	*cache.collection_game_parameters(lang=lang),
        ]

        random.shuffle(games)

        return Response(games)
