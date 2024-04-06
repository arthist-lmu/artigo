import random
import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from frontend import cache
from frontend.models import (
    Resource,
    Collection,
)

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class HomeView(APIView):
    def get(self, request, format=None):
        params = request.query_params

        lang = params.get('lang', 'de')

        collection_id = None
        resource_ids = None

        try:
            collection = Collection.objects \
                .filter(
                    titles__name__icontains=params['name'],
                    access='O',
                ) \
                .first()

            collection_id = collection.id
            resource_ids = Resource.objects \
                .filter(collection_id=collection_id) \
                .order_by('?') \
                .values_list('id', flat=True)[:25]
        except Exception:
            pass

        games = [
            *cache.random_game_parameters(
                lang=lang,
                collection_id=collection_id,
            ),
        ]

        if collection_id is None:
            games.extend(cache.collection_game_parameters(lang=lang))

        random.shuffle(games)

        if resource_ids is None:
            games.append({})
        else:
            games.append({
                'params': {
                    'resource_inputs': resource_ids,
                    'resource_type': 'custom_resource',
                    'resource_max_last_played': 0,
                },
            })

        return Response(games)
