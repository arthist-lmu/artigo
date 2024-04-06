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
        collection_ids = kwargs.get('collection_id', [])

        if not isinstance(langs, (list, set)):
            langs = [langs]

        if not isinstance(collection_ids, (list, set)):
            collection_ids = [collection_ids]

        if not len(collection_ids):
            values = Collection.objects \
                .filter(access='O') \
                .values_list('id', flat=True)

            collection_ids = [None, *values]

        for lang in langs:
            for collection_id in collection_ids:
                cache_name = f"{kwargs['name']}_{lang}_{collection_id}"
                values = cache.get(cache_name)

                if values is None or kwargs.get('renew'):
                    values = []

                    for variant in self.get_variants(lang):
                        params = (variant, lang, collection_id)
                        try:
                            values.append(self.create_game(*params))
                        except IndexError:
                            pass

                    timeout = kwargs.get('timeout', None)
                    cache.set(cache_name, values, timeout)

        return values

    @abstractmethod
    def create_game(self, *args):
        pass

    @staticmethod
    def get_params(tags=0, roi_tags=0):
        params = {}

        params['game_type'] = random.choice([
            'roi',
            'tagging',
        ])

        if params['game_type'] == 'roi':
            if tags == 0:
                params['game_type'] = 'tagging'
            elif roi_tags == 0:
                params['resource_min_roi_tags'] = 0
                params['opponent_type'] = 'no_opponent'
            else:
                # TODO: add suitable plugins
                pass

        if params['game_type'] == 'tagging':
            if tags == 0:
                params['resource_min_tags'] = 0
                params['opponent_type'] = 'no_opponent'
            else:
                params['taboo_type'] = random.choice([
                    'no_taboo',
                    'most_annotated_taboo',
                ])

                params['suggester_type'] = random.choice([
                    'no_suggester',
                    'cooccurrence_suggester',
                ])
        
        if not params.get('opponent_type'):
            params['opponent_type'] = random.choice([
                'no_opponent',
                'mean_gameround_opponent',
                'random_gameround_opponent',
            ])

        return params

    @abstractmethod
    def get_variants(self, lang):
        pass


class RandomGameParameters(GameParameters):
    def create_game(self, variant, lang, collection_id=None):
        game = {
            'type': variant['type'],
            'field': variant['field'],
        }

        annotations = {
            'tags': 0,
            'roi_tags': 0,
        }

        valid_resources = Resource.objects \
            .filter(enabled=True) \
            .exclude(hash_id__exact='')

        if collection_id is not None:
            valid_resources = valid_resources.filter(collection_id=collection_id)

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

            resources = valid_resources.values('id') \
                .annotate(
                    count_taggings=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__name__in=game['query'].values()),
                        ), 
                        0,
                    ),
                ) \
                .filter(count_taggings__gte=2)

            game['query'] = game['query'][lang]
            annotations['tags'] = 99
        elif game['field'] == 'creators':
            creators = valid_resources \
                .values(
                    'creators',
                    'creators__name',
                ) \
                .annotate(Count('creators')) \
                .order_by('-creators__count')

            creator = creators[random.randint(0, 49)]

            game['query'] = creator['creators__name']
            annotations['tags'] = 99

            resources = valid_resources.values('id') \
                .filter(creators__name=game['query']) \
                .annotate(
                    count_taggings=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__language=lang),
                        ), 
                        0,
                    ),
                ) \
                .filter(count_taggings__gt=0)
        elif game['field'] == 'resources':
            resources = valid_resources.values('id') \
                .annotate(
                    count_taggings=Coalesce(
                        Count(
                            'taggings__tag',
                            filter=Q(taggings__tag__language=lang),
                        ), 
                        0,
                    ),
                ) \
                .filter(count_taggings=0)

        resource_ids = list(resources.values_list('id', flat=True))
        random.shuffle(resource_ids)

        resource = Resource.objects.get(id=resource_ids[0])
        game['path'] = media_url_to_image(resource.hash_id)

        game['params'] = self.get_params(**annotations)
        game['params']['resource_inputs'] = resource_ids[:100]
        game['params']['resource_type'] = 'custom_resource'

        return game

    def get_variants(self, lang):
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
                'type': 'annotated-creator',
                'field': 'creators',
            },
        ]

        random.shuffle(values)

        return values


class CollectionGameParameters(GameParameters):
    def create_game(self, variant, lang, *args):
        game = {
            'path': variant['path'],
            'title': variant['title'],
        }

        annotations = {
            'tags': variant['count_taggings'],
            'roi_tags': variant['count_roi_taggings'],
        }

        resources = list(variant['resources'])
        random.shuffle(resources)

        game['params'] = self.get_params(**annotations)
        game['params']['resource_inputs'] = resources[:100]
        game['params']['resource_type'] = 'custom_resource'
        game['params']['resource_max_last_played'] = 0

        return game

    def get_variants(self, lang):
        values = Collection.objects.filter(access='O') \
            .filter(resources__enabled=True) \
            .annotate(
                count_resources=Coalesce(
                    Count('resources__id'),
                    0,
                ),
                resource_ids=ArrayAgg(
                    'resources__id',
                    distinct=True,
                ),
                count_taggings=Coalesce(
                    Count(
                        'resources__taggings__tag',
                        filter=Q(resources__taggings__tag__language=lang),
                    ),
                    0,
                ),
                count_roi_taggings=Coalesce(
                    Count(
                        'resources__rois__tag',
                        filter=Q(resources__rois__tag__language=lang),
                    ),
                    0,
                ),
            ) \
            .filter(count_resources__gte=0)

        values = Serializer(values, many=True).data
        random.shuffle(values)

        return values


@name
def random_game_parameters(**kwargs):
    return RandomGameParameters().run(**kwargs)


@name
def collection_game_parameters(**kwargs):
    return CollectionGameParameters().run(**kwargs)
