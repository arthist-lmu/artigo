import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend import cache

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class StatisticsView(APIView):
    def get(self, request, format=None):
        result = {
            **cache.statistics(),
            **cache.user_scores(),
        }

        return Response(result)
