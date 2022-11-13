import random
import logging

from django.core.cache import cache
from django.db.models import Count
from frontend.models import (
    CustomUser,
    Tag,
    Creator,
    Resource,
    Gameround,
    Gamesession,
    UserTagging,
)
from .utils import name

logger = logging.getLogger(__name__)


@name
def statistics(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        values = {
            'tags': {'n': Tag.objects.count()},
            'users': {'n': CustomUser.objects.count()},
            'creators': {'n': Creator.objects.count()},
            'taggings': {'n': UserTagging.objects.count()},
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
            .filter(tag__count__gte=25) \
            .order_by('-tag__count') \
            .values_list('tag__name', flat=True)

        tags = random.sample(list(tags), 25)
        values['tags']['names'] = tags

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
        values['creators']['names'] = creators

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
