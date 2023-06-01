import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from frontend.models import (
    CustomUser,
    UserROI,
    UserTagging,
)
from frontend.serializers import UserTaggingCountSerializer
from .utils import name

logger = logging.getLogger(__name__)


def get(created_gte, created_lt, limit=10):
    rois = UserROI.objects.values('user') \
        .filter(
            created__gte=created_gte,
            created__lt=created_lt,
            uploaded=False,
        ) \
        .annotate(
            sum_score=Sum('score'),
            sum_count=Count('tag'),
        ) \
        .values(
            'user_id',
            'user__username',
            'user__is_anonymous',
            'sum_score',
            'sum_count',
        )

    taggings = UserTagging.objects.values('user') \
        .filter(
            created__gte=created_gte,
            created__lt=created_lt,
            uploaded=False,
        ) \
        .annotate(
            sum_score=Sum('score'),
            sum_count=Count('tag'),
        ) \
        .values(
            'user_id',
            'user__username',
            'user__is_anonymous',
            'sum_score',
            'sum_count',
        )

    rois = UserTaggingCountSerializer(rois, many=True).data
    rois = {user['id']: user for user in rois}

    taggings = UserTaggingCountSerializer(taggings, many=True).data
    taggings = {user['id']: user for user in taggings}

    for user_id, tagging in taggings.items():
        if rois.get(user_id):
            tagging['sum_score'] += rois[user_id]['sum_score']
            tagging['sum_count'] += rois[user_id]['sum_count']

    for user_id, roi in rois.items():
        if not taggings.get(user_id):
            taggings[user_id] = roi

    taggings = sorted(
        taggings.values(),
        key=lambda x: x['sum_count'],
        reverse=True,
    ) 

    return taggings


@name
def user_scores(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        current_month = timezone.now().replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        previous_month = current_month - relativedelta(months=1)

        values = {
            'scores': {
                'current_month': get(
                    current_month,
                    datetime.today(),
                    limit=25,
                ),
                'previous_month': get(
                    previous_month,
                    current_month,
                    limit=1,
                ),
            },
        }

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
