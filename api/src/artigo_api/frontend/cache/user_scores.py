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
    users = CustomUser.objects.filter(is_staff=False) \
        .annotate(
            score_taggings=Coalesce(
                Sum(
                    'taggings__score',
                    filter=Q(taggings__created__gte=created_gte) \
                        & Q(taggings__created__lt=created_lt) \
                        & Q(taggings__uploaded=False),
                ), 
                0,
            ),
            count_taggings=Coalesce(
                Count(
                    'taggings__tag',
                    filter=Q(taggings__created__gte=created_gte) \
                        & Q(taggings__created__lt=created_lt) \
                        & Q(taggings__uploaded=False),
                ),
                0,
            ),
            score_roi_taggings=Coalesce(
                Sum(
                    'rois__score',
                    filter=Q(rois__created__gte=created_gte) \
                        & Q(rois__created__lt=created_lt) \
                        & Q(rois__uploaded=False),
                ),
                0,
            ),
            count_roi_taggings=Coalesce(
                Count(
                    'rois__tag',
                    filter=Q(rois__created__gte=created_gte) \
                        & Q(rois__created__lt=created_lt) \
                        & Q(rois__uploaded=False),
                ),
                0,
            ),
        ) \
        .annotate(
            sum_score=F('score_taggings') + F('score_roi_taggings'),
            sum_count=F('count_taggings') + F('count_roi_taggings'),
        ) \
        .order_by('-sum_count')[:max(1, limit)] \
        .values(
            'username',
            'is_anonymous',
            'sum_score',
            'sum_count',
        )

    return UserTaggingCountSerializer(users, many=True).data


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
                    limit=25,
                ),
            },
        }

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
