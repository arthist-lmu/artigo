import grpc
import logging
import traceback

from collections import defaultdict
from django.db.models import Count, F
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import *
from frontend.utils import to_int, to_float
from frontend.views.utils import ResourceViewHelper

logger = logging.getLogger(__name__)


class GameController:
    def __init__(
        self,
        resource_plugin_manager=None,
        opponent_plugin_manager=None,
        taboo_plugin_manager=None,
        suggester_plugin_manager=None,
    ):
        super().__init__()

        self.resource_plugin_manager = resource_plugin_manager
        self.opponent_plugin_manager = opponent_plugin_manager
        self.taboo_plugin_manager = taboo_plugin_manager
        self.suggester_plugin_manager = suggester_plugin_manager

    def __call__(self, params, user):
        if len(params) == 0:
            complete_gamesessions = Gameround.objects.filter(user=user) \
                .values('gamesession') \
                .annotate(count_gamerounds=Count('gamesession')) \
                .filter(count_gamerounds=F('gamesession__rounds')) \
                .values('gamesession')

            gamesession = Gamesession.objects.filter(user=user) \
                .exclude(gamesession__in=complete_gamesessions)

            if gamesession.count() > 1:
                return {'type': 'error', 'message': 'multiple_valid_gamesessions'}

            gamesession = gamesession.latest('created')
        elif params.get('session_id'):
            try:
                gamesession = Gamesession.objects.get(id=params['session_id'])
            except ObjectDoesNotExist:
                return {'type': 'error', 'message': 'invalid_gamesession'}
        else:
            result = self.create_game(params, user)
            if result['type'] == 'error': return result

            gamesession = result['gamesession']

        data = cache.get(f'gamesession_{gamesession.id}')

        if data is None:
            return {'type': 'error', 'message': 'outdated_gamesession'}

        if len(data['game']) == 0:
            cache.delete(f'gamesession_{gamesession.id}')

            return {'type': 'error', 'message': 'finished_gamesession'}

        try:
            gameround_data = list(data['game'].values())[0]

            gameround = Gameround(
                user=user,
                gamesession=gamesession,
                resource_id=gameround_data['resource_id'],
            )

            if data['query']['opponent_type'] is not None:
                opponent_type, _ = OpponentType.objects \
                    .get_or_create(name=data['query']['opponent_type'])
                opponent_type.save()

                gameround.opponent_type = opponent_type

            if data['query']['taboo_type'] is not None:
                taboo_type, _ = TabooType.objects \
                    .get_or_create(name=data['query']['taboo_type'])

                gameround.taboo_type = taboo_type

            gameround.save()

            if gameround_data.get('opponent_tags'):
                bulk_list = []

                for tag in gameround_data['opponent_tags']:
                    bulk_list.append(
                        OpponentTagging(
                            gameround=gameround,
                            resource=gameround.resource,
                            tag_id=tag.pop('id'),
                            created_after=tag['created_after'],
                        )
                    )

                OpponentTagging.objects.bulk_create(bulk_list)

            if gameround_data.get('taboo_tags'):
                bulk_list = []

                for tag in gameround_data['taboo_tags']:
                    bulk_list.append(
                        TabooTagging(
                            gameround=gameround,
                            resource=gameround.resource,
                            tag_id=tag.pop('id'),
                        )
                    )

                TabooTagging.objects.bulk_create(bulk_list)

            for name in data['query']['suggester_types']:
                suggester_type, _ = SuggesterType.objects \
                    .get_or_create(name=name)

                gameround.suggester_types.add(suggester_type)

            for name in data['query']['score_types']:
                score_type, _ = ScoreType.objects \
                    .get_or_create(name=name)

                gameround.score_types.add(score_type)
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'unknown_error'}

        data['game'].pop(gameround.resource_id)
        cache.set(f'gamesession_{gamesession.id}', data)

        logger.info(f'[Game Controller] Gameround: {gameround_data}')

        return {
            'type': 'ok',
            'session_id': gamesession.id,
            'rounds': gamesession.rounds,
            'round_id': gamesession.rounds - len(data['game']),
            'data': gameround_data,
        }

    def create_game(self, params, user):
        query = self.parse_query(params)
        logger.info(f'[Game Controller] Query: {query}')

        try:
            resource_ids = list(
                self.resource_plugin_manager.run(
                    {'user_id': user.id},
                    [query['resource_type']],
                    configs=[
                        {
                            'type': query['resource_type'],
                            'params': query['resource_options'],
                        },
                    ],
                ),
            )
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_game_options'}

        if resource_ids is None or len(resource_ids) == 0:
            return {'type': 'error', 'message': 'invalid_resources'}

        result = {}

        if query['opponent_type'] is not None:
            try:
                result['opponent'] = list(
                    self.opponent_plugin_manager.run(
                        resource_ids,
                        query['game_options'],
                        [query['opponent_type']],
                        configs=[
                            {
                                'type': query['opponent_type'],
                                'params': query['opponent_options'],
                            },
                        ],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_opponents'}

        if query['taboo_type'] is not None:
            try:
                result['taboo'] = list(
                    self.taboo_plugin_manager.run(
                        resource_ids,
                        query['game_options'],
                        [query['taboo_type']],
                        configs=[
                            {
                                'type': query['taboo_type'],
                                'params': query['taboo_options'],
                            },
                        ],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_taboos'}

            if len(query['suggester_types']) > 0:
                result['taboo'] = list(
                    self.suggester_plugin_manager.run(
                        result['taboo'],
                        query['game_options'],
                        query['suggester_types'],
                    ),
                )

        game = self.merge_to_game(result, resource_ids)
        # logger.info(f'[Game Controller] Game: {game}')

        try:
            gametype, _ = Gametype.objects.get_or_create(name='Tagging')

            gamesession = Gamesession(
                user=user,
                gametype=gametype,
                rounds=query['resource_options']['rounds'],
                round_duration=query['game_options']['round_duration'],
            )
            gamesession.save()
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_game_options'}

        timeout = None

        if query['game_options']['round_duration'] > 0:
            timeout = 60 * 60 * 24

        cache.set(
            f'gamesession_{gamesession.id}',
            {'query': query, 'game': game},
            timeout=timeout,
        )

        return {'type': 'ok', 'gamesession': gamesession}

    @staticmethod
    def parse_query(query):
        game_options = {
            'language': query.get('language', 'de'),
            'round_duration': to_int(query.get('round_duration'), 60),
        }

        resource_type = 'RandomResource'
        resource_options = {
            'rounds': to_int(query.get('rounds'), 5),
            'lt_percentile': to_float(query.get('lt_percentile'), 1.0),
            'max_last_played': to_int(query.get('max_last_played'), 6 * 30),
        }

        if query.get('resource_type'):
            if query['resource_type'] == 'random_resource':
                resource_type = 'RandomResource'

        opponent_type = None
        opponent_options = {}

        if query.get('opponent_type'):
            if query['opponent_type'] == 'mean_gameround_opponent':
                opponent_type = 'MeanGameroundOpponent'
            elif query['opponent_type'] == 'random_gameround_opponent':
                opponent_type = 'RandomGameroundOpponent'

        taboo_type = None
        taboo_options = {
            'max_tags': to_int(query.get('taboo_max_tags'), 5)
        }

        if query.get('taboo_type'):
            if query['taboo_type'] == 'most_annotated_taboo':
                taboo_type = 'MostAnnotatedTaboo'

        suggester_types = set()

        if query.getlist('suggester_types[]'):
            if 'cooccurrence_suggester' in query['suggester_types[]']:
                suggester_types.add('CooccurrenceSuggester')

        score_types = set()

        if query.getlist('score_types[]'):
            if 'annotation_validated_score' in query.getlist('score_types[]'):
                score_types.add('AnnotationValidatedScore')

            if 'opponent_validated_score' in query.getlist('score_types[]'):
                score_types.add('OpponentValidatedScore')

        result = {
            'game_options': game_options,
            'resource_type': resource_type,
            'resource_options': resource_options,
            'opponent_type': opponent_type,
            'opponent_options': opponent_options,
            'taboo_type': taboo_type,
            'taboo_options': taboo_options,
            'suggester_types': list(suggester_types),
            'score_types': list(score_types),
        }

        return result

    def merge_to_game(self, result, resource_ids):
        resources = ResourceView()(resource_ids)

        game = defaultdict(dict)

        for key, values in result.items():
            for value in values:
                resource_id = str(value.pop('resource_id', ''))

                if len(resource_id) == 0:
                    continue

                for field, v in value.items():
                    game[resource_id][f'{key}_{field}'] = v

                game[resource_id].update(resources[resource_id])

        return dict(game)


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
