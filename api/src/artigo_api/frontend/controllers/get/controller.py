import logging
import traceback

from collections import defaultdict
from django.db.models import Count, F
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import *
from frontend.utils import to_boolean, to_type, is_in, media_url_to_image
from frontend.views.utils import ResourceViewHelper
from ..utils import get_configs

logger = logging.getLogger(__name__)


class GameController:
    def __init__(self):
        super().__init__()

        self.plugins = cache.get('plugins', {})

    def __call__(self, params, user):
        if len(params) == 0:
            complete_gamesession_ids = Gameround.objects.filter(user=user) \
                .values('gamesession') \
                .annotate(count_gamerounds=Count('gamesession')) \
                .filter(count_gamerounds=F('gamesession__rounds')) \
                .values('gamesession_id')

            gamesession = Gamesession.objects.filter(user=user) \
                .exclude(id__in=complete_gamesession_ids)

            if gamesession.count() > 1:
                return {'type': 'error', 'message': 'multiple_valid_gamesessions'}

            try:
                gamesession = gamesession.latest('created')
            except:
                return {'type': 'error', 'message': 'no_valid_gamesessions'}
        elif params.get('session_id'):
            try:
                gamesession = Gamesession.objects.get(id=params['session_id'])
            except ObjectDoesNotExist:
                return {'type': 'error', 'message': 'invalid_gamesession'}
        else:
            result = self.create_gamesession(params, user)
            if result['type'] == 'error': return result

            gamesession = result['gamesession']

        gamesession_data = cache.get(f'gamesession_{gamesession.id}')

        if gamesession_data is None:
            return {'type': 'error', 'message': 'outdated_gamesession'}

        if len(gamesession_data['game']) == 0:
            cache.delete(f'gamesession_{gamesession.id}')

            return {'type': 'error', 'message': 'finished_gamesession'}

        gameround_data = list(gamesession_data['game'].values())[0]

        try:
            gameround = self.create_gameround(
                resource_id=gameround_data['resource_id'],
                query=gamesession_data['query'],
                gamesession=gamesession,
                user=user,
            )

            self.fill_gameround(gameround, gameround_data)
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'unknown_error'}

        gamesession_data['game'].pop(gameround.resource_id)
        cache.set(f'gamesession_{gamesession.id}', gamesession_data)

        return {
            'type': 'ok',
            'session_id': gamesession.id,
            'rounds': gamesession.rounds,
            'round_id': gamesession.rounds - len(gamesession_data['game']),
            'data': gameround_data,
        }

    def create_gamesession(self, params, user):
        query = self.parse_query(params)
        logger.info(f'[Game Controller] Query: {query}')

        try:
            resource_ids = list(
                self.plugins['resource'].run(
                    {'user_id': user.id},
                    query['resource_type'],
                    configs=get_configs(query, 'resource'),
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
                    self.plugins['opponent'].run(
                        resource_ids,
                        query['game_options'],
                        query['opponent_type'],
                        configs=get_configs(query, 'opponent'),
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_opponents'}

        if query.get('input_type') is not None:
            try:
                result['input'] = list(
                    self.plugins['input'].run(
                        resource_ids,
                        query['game_options'],
                        query['input_type'],
                        configs=get_configs(query, 'input'),
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_inputs'}

        if query.get('taboo_type') is not None:
            try:
                result['taboo'] = list(
                    self.plugins['taboo'].run(
                        resource_ids,
                        query['game_options'],
                        query['taboo_type'],
                        configs=get_configs(query, 'taboo'),
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_taboos'}

        game = self.merge_to_game(
            result,
            resource_ids,
            query['retrieve_metadata'],
        )
        logger.info(f'[Game Controller] Game: {game}')

        try:
            game_type, _ = GameType.objects \
                .get_or_create(name=self._type)
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

    @staticmethod
    def create_gameround(resource_id, query, gamesession, user):
        gameround = Gameround(
            user=user,
            gamesession=gamesession,
            resource_id=resource_id,
        )

        for name in query.get('opponent_type', []):
            opponent_type, _ = OpponentType.objects \
                .get_or_create(name=name)
            opponent_type.save()

            gameround.opponent_type = opponent_type

        for name in query.get('input_type', []):
            input_type, _ = InputType.objects \
                .get_or_create(name=name)
            input_type.save()

            gameround.input_type = input_type

        for name in query.get('taboo_type', []):
            taboo_type, _ = TabooType.objects \
                .get_or_create(name=name)
            taboo_type.save()

            gameround.taboo_type = taboo_type

        gameround.save()

        for name in query.get('suggester_type', []):
            suggester_type, _ = SuggesterType.objects \
                .get_or_create(name=name)

            gameround.suggester_types.add(suggester_type)

        for name in query.get('score_type', []):
            score_type, _ = ScoreType.objects \
                .get_or_create(name=name)

            gameround.score_types.add(score_type)

        return gameround

    @staticmethod
    def fill_gameround(gameround, data):
        pass

    def parse_query(self, query):
        result = defaultdict(list)
        result['game_options'] = {
            'round_duration': 60,
        }

        for key, value in query.items():
            if key.startswith('game_'):
                key = key.strip().split('_', 1)[-1]

                if not key in ['type', 'type[]']:
                    result['game_options'][key] = to_type(value)

        for plugin_name, plugin_manager in self.plugins.items():
            plugin_type = f'{plugin_name}_type'
            plugin_options = f'{plugin_name}_options'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(self._type, config['game_types']):
                        values = query.get(plugin_type)

                        if values is None:
                            values = query.getlist(f'{plugin_type}[]')
                            
                        if values is not None:
                            if is_in(config['name'], values):
                                result[plugin_type].append(config['type'])
                        elif config.get('default', False):
                            result[plugin_type].append(config['type'])

            if result.get(plugin_type):
                result[plugin_options] = {}

                for key, value in query.items():
                    if key.startswith(f'{plugin_name}_'):
                        if key.endswith('[]'):
                            value = query.getlist(key)
                            key = key.strip()[:-2]

                        key = key.split('_', 1)[-1]

                        if key.lower() != 'type':
                            result[plugin_options][key] = to_type(value)

        value = query.get('retrieve_metadata', False)
        result['retrieve_metadata'] = to_boolean(value)

        return dict(result)

    def merge_to_game(self, result, resource_ids, retrieve_metadata=False):
        game = defaultdict(dict)

        if retrieve_metadata:
            resources = ResourceView()(resource_ids)
        else:
            resources = Resource.objects \
                .filter(id__in=resource_ids) \
                .values(
                    'id',
                    'hash_id',
                )

            resources = {
                str(x['id']): {
                    'resource_id': str(x['id']),
                    'path': media_url_to_image(x['hash_id']),
                }
                for x in list(resources)
            }

        for key, values in result.items():
            for value in values:
                if value.get('resource_id') is None:
                    continue

                resource_id = str(value.pop('resource_id'))

                for field, v in value.items():
                    game[resource_id][f'{key}_{field}'] = v

                if game.get(resource_id) is None:
                    game[resource_id] = {}

                game[resource_id].update(resources[resource_id])

        return dict(game)


class ResourceView(ResourceViewHelper):
    def __call__(self, resource_ids):
        params = {'ids': map(str, resource_ids)}

        return self.rpc_get(params)
