import logging
import traceback

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.models import UserTagging
from frontend.serializers import UserTaggingCountSerializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class HighscoreView(APIView):
    def count(self, taggings, created_gte=None, created_lt=None, limit=10):
        if created_gte is not None:
            taggings = taggings.filter(created__gte=created_gte)

        if created_lt is not None:
            taggings = taggings.filter(created__lt=created_lt)

        users = taggings.values('user').annotate(
                count_taggings=Count('user'),
                count_gamerounds=Count('gameround', distinct=True),
            ) \
            .order_by('-count_taggings')[:max(1, limit)] \
            .values(
                'user__username',
                'count_taggings',
                'count_gamerounds',
            )

        return UserTaggingCountSerializer(users, many=True).data

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        limit = request.query_params.get('limit', 10)

        current = datetime.today().replace(day=1)
        previous = current - relativedelta(months=1)

        try:
            taggings = UserTagging.objects.exclude(user__username=None)

            data = {
                'alltime': self.count(taggings, limit=limit),
                'current': self.count(taggings, current, limit=limit),
                'previous': self.count(taggings, previous, current, limit),
            }

            return Response(data)
        except Exception as error:
            logger.error(traceback.format_exc())

        raise APIException('unknown_error')
