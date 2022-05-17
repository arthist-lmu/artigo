import grpc
import logging
import traceback

from collections import defaultdict
from django.db.models import Count, F
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import *
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
            result = self.create_gamesession(params, user)
            if result['type'] == 'error': return result

            gamesession = result['gamesession']

        data = cache.get(f'gamesession_{gamesession.id}')

        if data is None:
            return {'type': 'error', 'message': 'outdated_gamesession'}

        if len(data['game']) == 0:
            cache.delete(f'gamesession_{gamesession.id}')

            return {'type': 'error', 'message': 'finished_gamesession'}

        try:
            gameround = self.create_gameround(
                query=data['query'],
                data=list(data['game'].values())[0],
                gamesession=gamesession,
                user=user,
            )
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'unknown_error'}

        data['game'].pop(gameround.resource_id)
        cache.set(f'gamesession_{gamesession.id}', data)

        return {
            'type': 'ok',
            'session_id': gamesession.id,
            'rounds': gamesession.rounds,
            'round_id': gamesession.rounds - len(data['game']),
            'data': list(data['game'].values())[0],
        }

    def create_gamesession(self, params, user):
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

        if query.get('opponent_type') is not None:
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

        if query.get('taboo_type') is not None:
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

            if len(query.get('suggester_types', [])) > 0:
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
            game_type, _ = GameType.objects \
                .get_or_create(name=query['game_type'])
            game_type.save()

            gamesession = Gamesession(
                user=user,
                game_type=game_type,
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

        return {
            'type': 'ok',
            'gamesession': gamesession,
        }

    @staticmethod
    def create_gameround(query, data, gamesession, user):
        pass

    @staticmethod
    def parse_query(query):
        pass

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
