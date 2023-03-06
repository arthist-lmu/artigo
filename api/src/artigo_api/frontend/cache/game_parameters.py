import random
import logging

from abc import ABC, abstractmethod
from itertools import cycle
from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.contrib.postgres.aggregates import ArrayAgg
from frontend.utils import media_url_to_image
from frontend.models import (
    Resource,
    Collection,
    UserTagging,
)
from frontend.serializers import CollectionCountSerializer as Serializer
from .utils import name

logger = logging.getLogger(__name__)


class GameParameters(ABC):
    def run(self, **kwargs):
        langs = kwargs.get('lang', ['de', 'en'])

        if not isinstance(langs, (list, set)):
            langs = [langs]

        for lang in langs:
            cache_name = f"{kwargs['name']}_{lang}"
            values = cache.get(cache_name)

            if values is None or kwargs.get('renew'):
                values = self.get_values()
                variants = self.get_variants()

                if len(variants) < len(values):
                    values = values[:len(variants)]

                for variant, game in zip(variants, cycle(values)):
                    while game.get('path') is None:
                        try:
                            game = self.create_game(game, variant, lang)
                        except IndexError:
                            pass

                timeout = kwargs.get('timeout', None)
                cache.set(cache_name, values, timeout)

        return values

    @abstractmethod
    def create_game(self):
        pass

    @abstractmethod
    def get_values(self):
        pass

    @abstractmethod
    def get_variants(self):
        pass


class RandomGameParameters(GameParameters):
    def create_game(self, game, variant, lang):
        game['type'] = variant['type']
        game['field'] = variant['field']

        if game['field'] == 'tags':
            if game['type'] == 'annotated-color':
                colors = [
                    { 'de': 'schwarz',           'en': 'black' },
                    { 'de': 'weiß',              'en': 'white'} ,
                    { 'de': 'grau',              'en': 'grey' },
                    { 'de': 'rot',               'en': 'red' },
                    { 'de': 'blau',              'en': 'blue' },
                    { 'de': 'braun',             'en': 'brown' },
                    { 'de': 'grün',              'en': 'green' },
                    { 'de': 'gelb',              'en': 'yellow' },
                ]

                game['query'] = random.choice(colors)
            elif game['type'] == 'annotated-epoch':
                epochs = [
                    { 'de': 'renaissance',       'en': 'renaissance' },
                    { 'de': 'manierismus',       'en': 'mannerism' },
                    { 'de': 'barock',            'en': 'baroque' },
                    { 'de': 'rokoko',            'en': 'rococo' },
                    { 'de': 'romantik',          'en': 'romanticism' },
                    { 'de': 'realismus',         'en': 'realism' },
                    { 'de': 'impressionismus',   'en': 'impressionism' },
                    { 'de': 'pointillismus',     'en': 'pointillism' },
                    { 'de': 'symbolismus',       'en': 'symbolism' },
                    { 'de': 'expressionismus',   'en': 'expressionism' },
                    { 'de': 'kubismus',          'en': 'cubism' },
                ]

                game['query'] = random.choice(epochs)
            else:
                tags = UserTagging.objects \
                    .filter(tag__language=lang) \
                    .values(
                        'tag',
                        'tag__name',
                    ) \
                    .annotate(Count('tag')) \
                    .order_by('-tag__count')

                tag = tags[random.randint(0, 149)]
                game['query'] = {lang: tag['tag__name']}

            resources = UserTagging.objects \
                .exclude(resource__hash_id__exact='') \
                .filter(tag__name__in=game['query'].values()) \
                .values('resource') \
                .annotate(Count('resource')) \
                .filter(resource__count__gte=2) \
                .values_list('resource', flat=True)

            game['query'] = game['query'][lang]
        elif game['field'] == 'creators':
            creators = Resource.objects \
                .values(
                    'creators',
                    'creators__name',
                ) \
                .annotate(Count('creators')) \
                .order_by('-creators__count')

            creator = creators[random.randint(0, 49)]
            game['query'] = creator['creators__name']

            resources = Resource.objects \
                .exclude(hash_id__exact='') \
                .filter(creators=creator['creators']) \
                .values_list('id', flat=True)
        elif game['field'] == 'resources':
            resources = Resource.objects.values('id') \
                .exclude(hash_id__exact='') \
                .annotate(
                    count_taggings=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__language=lang),
                        ),
                        0,
                    ),
                ) \
                .filter(count_taggings=0) \
                .values_list('id', flat=True)

            game['params']['resource_min_tags'] = 0
            game['params']['opponent_type'] = 'no_opponent'

            game['params'].pop('taboo_type', None)

        resources = list(resources)
        random.shuffle(resources)

        resource = Resource.objects.get(id=resources[0])
        game['path'] = media_url_to_image(resource.hash_id)

        game['params']['resource_inputs'] = resources[:100]
        game['params']['resource_type'] = 'custom_resource'

        return game

    def get_values(self):
        values = [
            {
                'params': {
                    'game_type': 'roi',
                    'game_min_roi_tags': 0,
                },
            },
            {
                'params': {
                    'game_type': 'tagging',
                },
            },
            {
                'params': {
                    'game_type': 'tagging',
                    'taboo_type': 'most_annotated_taboo',
                },
            },
        ]

        random.shuffle(values)

        return values

    def get_variants(self):
        values = [
            {
                'type': 'annotated-color',
                'field': 'tags',
            },
            {
                'type': 'annotated-epoch',
                'field': 'tags',
            },
            {
                'type': 'not-annotated',
                'field': 'resources',
            },
            {
                'type': 'most-annotated',
                'field': 'creators',
            },
        ]

        return values


class CollectionGameParameters(GameParameters):
    def create_game(self, game, variant, lang):
        resources = list(variant['resources'])
        random.shuffle(resources)

        game['path'] = variant['path']
        game['title'] = variant['title']

        game['params']['resource_inputs'] = resources[:100]
        game['params']['resource_type'] = 'custom_resource'

        return game

    def get_values(self):
        values = [
            {
                'params': {
                    'game_type': 'roi',
                    'resource_min_roi_tags': 0,
                },
            },
            {
                'params': {
                    'game_type': 'tagging',
                },
            },
            {
                'params': {
                    'game_type': 'tagging',
                    'opponent_type': 'no_opponent',
                },
            },
        ]

        random.shuffle(values)

        return values

    def get_variants(self):
        values = Collection.objects.filter(access='O') \
            .annotate(
                count_resources=Coalesce(Count('resources__id'), 0),
                resource_ids=ArrayAgg('resources__id'),
            ) \
            .filter(count_resources__gte=0)

        values = Serializer(values, many=True).data

        return values


@name
def random_game_parameters(**kwargs):
    return RandomGameParameters().run(**kwargs)


@name
def collection_game_parameters(**kwargs):
    return CollectionGameParameters().run(**kwargs)
