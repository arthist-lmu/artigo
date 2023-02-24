import random
import logging

from django.core.cache import cache
from django.db.models import Count
from frontend.utils import media_url_to_image
from frontend.models import (
    Resource,
    UserTagging,
)
from .utils import name

logger = logging.getLogger(__name__)


@name
def random_game_parameters(**kwargs):
    def create_game(game, variant, lang):
        game['type'] = variant['type']
        game['field'] = variant['field']

        if game['field'] == 'tags':
            if game['type'] == 'color':
                colors = [
                    {'de': 'schwarz',           'en': 'black'},
                    {'de': 'weiß',              'en': 'white'},
                    {'de': 'grau',              'en': 'grey'},
                    {'de': 'rot',               'en': 'red'},
                    {'de': 'blau',              'en': 'blue'},
                    {'de': 'braun',             'en': 'brown'},
                    {'de': 'grün',              'en': 'green'},
                    {'de': 'gelb',              'en': 'yellow'},
                ]

                game['query'] = random.choice(colors)
            elif game['type'] == 'epoch':
                epochs = [
                    {'de': 'renaissance',       'en': 'renaissance'},
                    {'de': 'manierismus',       'en': 'mannerism'},
                    {'de': 'barock',            'en': 'baroque'},
                    {'de': 'rokoko',            'en': 'rococo'},
                    {'de': 'romantik',          'en': 'romanticism'},
                    {'de': 'realismus',         'en': 'realism'},
                    {'de': 'impressionismus',   'en': 'impressionism'},
                    {'de': 'pointillismus',     'en': 'pointillism'},
                    {'de': 'symbolismus',       'en': 'symbolism'},
                    {'de': 'expressionismus',   'en': 'expressionism'},
                    {'de': 'kubismus',          'en': 'cubism'},
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
        elif game['field'] == 'meta.creators':
            creators = Resource.objects \
                .exclude(hash_id__exact='') \
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

        resources = list(resources)
        random.shuffle(resources)

        game['params']['resource_inputs'] = resources[:100]
        game['params']['resource_type'] = 'custom_resource'

        resource = Resource.objects.get(id=resources[0])
        game['path'] = media_url_to_image(resource.hash_id)

        return game

    def get_variants():
        values = [
            {
                'type': 'color',
                'field': 'tags',
            },
            {
                'type': 'epoch',
                'field': 'tags',
            },
            {
                'type': 'creator',
                'field': 'meta.creators',
            },
        ]

        random.shuffle(values)

        return values

    langs = kwargs.get('lang', 'de,en').split(',')

    for lang in langs:
        values = cache.get(f"{kwargs['name']}_{lang}")

        if values is None or kwargs.get('renew'):
            values = [
                {
                    'params': {
                        'game_type': 'roi',
                        'min_roi_tags': 0,
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

            for game, variant in zip(values, get_variants()):
                while game.get('path') is None:
                    try:
                        game = create_game(game, variant, lang)
                    except IndexError:
                        pass

            random.shuffle(values)

            timeout = kwargs.get('timeout', None)
            cache.set(f"{kwargs['name']}_{lang}", values, timeout)

    return values
