import logging
import traceback

from frontend.models import Tagging
from frontend.serializers import UserTaggingCountSerializer
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class Highscore(APIView):
    def count(self, taggings, created=None, limit=10):
        if created is not None:
            taggings = taggings.filter(created__gte=created)

        users = taggings.values('user').annotate(
            count_taggings=Count('user'),
            count_gamerounds=Count('gameround', distinct=True),
        )
        users = users.order_by('-count_taggings')[:max(1, limit)]
        users = users.values(
            'user__username',
            'count_taggings',
            'count_gamerounds',
        )

        return UserTaggingCountSerializer(users, many=True).data

    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        limit = request.query_params.get('limit', 10)

        current = datetime.today().replace(day=1)
        previous = current - relativedelta(months=1)

        data = {}

        try:
            taggings = Tagging.objects.exclude(user__username=None)
            data['alltime'] = self.count(taggings, limit=limit)

            taggings_current = taggings.filter(created__gte=current)
            data['current'] = self.count(taggings_current, limit=limit)

            taggings_previous = taggings.filter(
                created__gte=previous,
                created__lt=current,
            )
            data['previous'] = self.count(taggings_previous, limit=limit)

            return Response(data)
        except Exception as e:
            logger.error(traceback.format_exc())

        raise APIException('Highscore could not be processed.')
