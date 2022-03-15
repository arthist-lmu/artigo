import logging

from datetime import timedelta
from django.db.models import Count, OuterRef, Subquery, F
from frontend.models import Tagging
from frontend.plugins import (
    OpponentPlugin,
    OpponentPluginManager,
)
from frontend.serializers import OpponentSerializer

logger = logging.getLogger(__name__)


@OpponentPluginManager.export('RandomGameroundOpponent')
class RandomGameroundOpponent(OpponentPlugin):
    default_config = {
        'min_tags': 5,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.min_tags = self.config['min_tags']

    def __call__(self, resource_ids, params):
        # TODO: filter by game_type (taboo etc.)
        round_duration = params.get('round_duration', 0)

        gamerounds = Tagging.objects.filter(
                resource=OuterRef('resource'),
                gameround__gamesession__round_duration__gte=round_duration,
                tag__language=params.get('language', 'de'),
            ) \
            .values('gameround') \
            .annotate(count_tags=Count('tag', distinct=True)) \
            .filter(count_tags__gte=self.min_tags) \
            .order_by('?') \
            .values('gameround')[:1]

        taggings = Tagging.objects.filter(resource_id__in=resource_ids) \
            .filter(gameround__in=Subquery(gamerounds)) \
            .annotate(created_after=F('created') - F('gameround__created')) \
            .filter(created_after__lt=timedelta(seconds=round_duration)) \
            .order_by('resource', 'created_after') \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
                'created_after',
            )

        return OpponentSerializer(taggings, many=True).data
