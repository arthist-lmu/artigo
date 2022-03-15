import logging

from datetime import timedelta
from django.db.models import Count, OuterRef, Subquery, F, Avg
from frontend.models import Tagging
from frontend.plugins import (
    OpponentPlugin,
    OpponentPluginManager,
)
from frontend.serializers import OpponentSerializer

logger = logging.getLogger(__name__)


@OpponentPluginManager.export('MeanGameroundOpponent')
class MeanGameroundOpponent(OpponentPlugin):
    default_config = {}
    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, resource_ids, params):
        # TODO: filter by game_type (taboo etc.)
        round_duration = params.get('round_duration', 0)

        taggings = Tagging.objects.filter(
                resource_id__in=resource_ids,
                gameround__gamesession__round_duration__gte=round_duration,
                tag__language=params.get('language', 'de'),
            )\
            .annotate(created_after_tag=F('created') - F('gameround__created'))

        limits = taggings.values('resource') \
            .annotate(
                count_taggings=Count('tag'),
                count_gamerounds=Count('gameround', distinct=True),
            ) \
            .annotate(n=F('count_taggings') / F('count_gamerounds')) \
            .values('resource_id', 'n')

        taggings = taggings.values('resource', 'tag') \
            .annotate(
                count_taggings=Count('tag'),
                count_gamerounds=Count('gameround', distinct=True),
                created_after=Avg(F('created_after_tag')),
            ) \
            .annotate(p=F('count_taggings') / F('count_gamerounds')) \
            .filter(
                p__gte=0.5,
                created_after__lt=timedelta(seconds=round_duration),
            ) \
            .order_by('resource', 'p') \
            .values(
                'resource_id',
                'tag_id',
                'tag__name',
                'created_after',
            )

        limits = {x['resource_id']: x['n'] for x in limits}
        opponents = OpponentSerializer(taggings, many=True).data

        for opponent in opponents:
            limit = limits[opponent['resource_id']]
            
            opponent['tags'] = opponent['tags'][:int(limit)]
            opponent['tags'].sort(key=lambda x: x['created_after'])

        return opponents