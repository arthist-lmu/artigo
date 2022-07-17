import random
import logging
import traceback

from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.utils import media_url_to_image
from frontend.models import (
    Resource,
    UserTagging,
)

logger = logging.getLogger(__name__)

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


@extend_schema(methods=['GET'], exclude=True)
class HomeView(APIView):
    @property
    def variants(self):
        values = [
            # { 'type': 'tag', 'field': 'tags' },
            { 'type': 'color', 'field': 'tags' },
            { 'type': 'epoch', 'field': 'tags' },
            { 'type': 'creator', 'field': 'meta.creators' },
        ]

        random.shuffle(values)

        return values

    def create(self, game, variant, lang='de'):
        game['type'] = variant['type']
        game['field'] = variant['field']

        if game['field'] == 'tags':
            if game['type'] == 'color':
                game['query'] = random.choice(colors)
            elif game['type'] == 'epoch':
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

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        games = [
            {
                'params': {
                    'game_type': 'roi',
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

        lang = request.query_params.get('lang', 'de')

        for game, variant in zip(games, self.variants):
            while game.get('path') is None:
                try:
                    game = self.create(game, variant, lang)
                except IndexError:
                    pass

        random.shuffle(games)

        return Response(games)
