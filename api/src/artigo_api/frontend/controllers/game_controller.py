import logging
import traceback

from collections import defaultdict
from django.db.models import Count, F
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import *
from frontend.utils import to_type, is_in
from frontend.views.utils import ResourceViewHelper

logger = logging.getLogger(__name__)


class GameController:
    def __init__(
        self,
        resource_plugin_manager=None,
        opponent_plugin_manager=None,
        taboo_plugin_manager=None,
        suggester_plugin_manager=None,
        score_plugin_manager=None,
    ):
        super().__init__()

        self.resource_plugin_manager = resource_plugin_manager
        self.opponent_plugin_manager = opponent_plugin_manager
        self.taboo_plugin_manager = taboo_plugin_manager
        self.suggester_plugin_manager = suggester_plugin_manager
        self.score_plugin_manager = score_plugin_manager

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

        gameround_data = list(data['game'].values())[0]

        try:
            gameround = self.create_gameround(
                query=data['query'],
                data=gameround_data,
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
            'data': gameround_data,
        }

    def create_gamesession(self, params, user):
        query = self.parse_query(params)
        logger.info(f'[Game Controller] Query: {query}')

        try:
            resource_ids = list(
                self.resource_plugin_manager.run(
                    {'user_id': user.id},
                    query['resource_type'],
                    configs=[
                        {
                            'type': resource_type,
                            'params': query['resource_options'],
                        }
                        for resource_type in query['resource_type']
                    ],
                )
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
                        query['opponent_type'],
                        configs=[
                            {
                                'type': opponent_type,
                                'params': query['opponent_options'],
                            }
                            for opponent_type in query['opponent_type']
                        ],
                    )
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
                        query['taboo_type'],
                        configs=[
                            {
                                'type': taboo_type,
                                'params': query['taboo_options'],
                            }
                            for taboo_type in query['taboo_type']
                        ],
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_taboos'}

            if len(query.get('suggester_type', [])) > 0:
                result['taboo'] = list(
                    self.suggester_plugin_manager.run(
                        result['taboo'],
                        query['game_options'],
                        query['suggester_type'],
                    )
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
                rounds=len(game),
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

    def parse_query(self, query):
        result = defaultdict(list)

        result['game_type'] = query.get('game_type', 'tagging')
        result['game_options'] = {}

        for key, value in query.items():
            if key.startswith('game_'):
                key = key.strip().split('_', 1)[-1]

                if not key in ['type', 'type[]']:
                    result['game_options'][key] = to_type(value)

        plugins = {
            'resource': self.resource_plugin_manager,
            'opponent': self.opponent_plugin_manager,
            'taboo': self.taboo_plugin_manager,
            'suggester': self.suggester_plugin_manager,
            'score': self.score_plugin_manager,
        }

        for plugin_name, plugin_manager in plugins.items():
            plugin_type = f'{plugin_name}_type'
            plugin_options = f'{plugin_name}_options'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(result['game_type'], config['game_types']):
                        values = query.get(plugin_type)

                        if values is None:
                            values = query.getlist(f'{plugin_type}[]')
                            
                        if values:
                            if is_in(config['name'], values):
                                result[plugin_type].append(config['type'])
                        elif config.get('default', False):
                            result[plugin_type].append(config['type'])

            if result.get(plugin_type):
                result[plugin_options] = {}

                for key, value in query.items():
                    if key.startswith(f'{plugin_name}_'):
                        key = key.strip().split('_', 1)[-1]

                        if not key in ['type', 'type[]']:
                            result[plugin_options][key] = to_type(value)

        return dict(result)

    def merge_to_game(self, result, resource_ids):
        game = defaultdict(dict)

        resources = ResourceView()(resource_ids)

        for key, values in result.items():
            for value in values:
                if value.get('resource_id') is None:
                    continue

                resource_id = str(value.pop('resource_id'))

                for field, v in value.items():
                    game[resource_id][f'{key}_{field}'] = v

                game[resource_id].update(resources[resource_id])

        return dict(game)


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
