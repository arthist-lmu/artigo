import random
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
from frontend.models import (
    CustomUser,
    Tag,
    Creator,
    Resource,
    Gameround,
    Gamesession,
    UserROI,
    UserTagging,
)
from frontend.serializers import UserTaggingCountSerializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET'], exclude=True)
class ScoresView(APIView):
    def count(self, taggings, created_gte=None, created_lt=None, limit=10):
        if created_gte is not None:
            taggings = taggings.filter(created__gte=created_gte)

        if created_lt is not None:
            taggings = taggings.filter(created__lt=created_lt)

        users = taggings.values('user') \
            .annotate(
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
            taggings = UserTagging.objects.filter(
                user__is_anonymous=False,
                uploaded=False,
            )

            result = {
                'alltime': self.count(taggings, limit=limit),
                'current': self.count(taggings, current, limit=limit),
                'previous': self.count(taggings, previous, current, limit),
            }

            return Response(result)
        except Exception as error:
            logger.error(traceback.format_exc())

        raise APIException('unknown_error')


@extend_schema(methods=['GET'], exclude=True)
class StatisticsView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        result = {
            'tags': {'n': Tag.objects.count()},
            'users': {'n': CustomUser.objects.count()},
            'creators': {'n': Creator.objects.count()},
            'resources': {'n': Resource.objects.count()},
            'gamerounds': {'n': Gameround.objects.count()},
            'gamesessions': {'n': Gamesession.objects.count()},
        }

        tags = UserTagging.objects \
            .values(
                'tag',
                'tag__name'
            ) \
            .annotate(Count('tag')) \
            .filter(tag__count__gte=10) \
            .order_by('-tag__count') \
            .values_list('tag__name', flat=True)

        tags = random.sample(list(tags), 25)
        result['tags']['names'] = tags

        creators = Resource.objects \
            .values(
                'creators',
                'creators__name'
            ) \
            .annotate(Count('creators')) \
            .filter(creators__count__gte=25) \
            .order_by('-creators__count') \
            .values_list('creators__name', flat=True)

        creators = random.sample(list(creators), 25)
        result['creators']['names'] = creators

        return Response(result)
