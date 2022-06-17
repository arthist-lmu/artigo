import logging

from datetime import timedelta
from django.db.models import Count, F
from frontend.models import UserROI
from frontend.plugins import (
    OpponentPlugin,
    OpponentPluginManager,
)
from frontend.serializers import OpponentROISerializer
from .utils import gamerounds_per_resource

logger = logging.getLogger(__name__)


@OpponentPluginManager.export('RandomGameroundROIOpponent')
class RandomGameroundTaggingOpponent(OpponentPlugin):
    default_config = {
        'min_tags': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.min_tags = self.config['min_tags']

    def __call__(self, resource_ids, params):
        round_duration = params.get('round_duration', 0)

        gamerounds = UserROI.objects.filter(
                resource_id__in=resource_ids,
                gameround__gamesession__round_duration__gte=round_duration,
                tag__language=params.get('language', 'de'),
            ) \
            .values('gameround') \
            .annotate(count_tags=Count('tag', distinct=True)) \
            .filter(count_tags__gte=self.min_tags) \
            .order_by('?') \
            .values(
                'gameround_id',
                'resource_id',
            )

        gameround_ids = gamerounds_per_resource(gamerounds, resource_ids)

        taggings = UserROI.objects.filter(gameround_id__in=gameround_ids) \
            .annotate(created_after=F('created') - F('gameround__created')) \
            .filter(created_after__lt=timedelta(seconds=round_duration)) \
            .order_by('resource', 'created_after') \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
                'x',
                'y',
                'width',
                'height',
                'created_after',
            )

        opponents = OpponentROISerializer(
            taggings,
            many=True,
            context={'ids': resource_ids}
        ).data

        return opponents
