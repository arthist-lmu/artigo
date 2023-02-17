import time
import logging
import traceback

from collections import defaultdict
from django.db.models import Count, F
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from frontend.models import *
from frontend import cache as frontend_cache
from frontend.utils import (
    is_in,
    to_type,
    to_boolean,
    media_url_to_image,
    upload_url_to_image,
)
from ..utils import get_configs

logger = logging.getLogger(__name__)


class GameController:
    def __init__(self):
        super().__init__()

        self.plugins = frontend_cache.plugins()

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
                return {
                    'type': 'error',
                    'message': 'multiple_valid_gamesessions',
                }

            try:
                gamesession = gamesession.latest('created')
            except:
                return {
                    'type': 'error',
                    'message': 'gamesessions_are_invalid',
                }
        elif params.get('session_id'):
            try:
                gamesession = Gamesession.objects.get(id=params['session_id'])
            except ObjectDoesNotExist:
                return {
                    'type': 'error',
                    'message': 'gamesession_is_invalid',
                }
        else:
            result = self.create_gamesession(params, user)
            if result['type'] == 'error': return result

            gamesession = result['gamesession']

        gamesession_data = cache.get(f'gamesession_{gamesession.id}')

        if gamesession_data is None:
            return {
                'type': 'error',
                'message': 'gamesession_is_outdated',
            }

        if len(gamesession_data['game']) == 0:
            cache.delete(f'gamesession_{gamesession.id}')

            return {
                'type': 'error',
                'message': 'gamesession_is_outdated',
            }

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

            return {
                'type': 'error',
                'message': 'unknown_error',
            }

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

            return {
                'type': 'error',
                'message': 'game_options_are_invalid',
            }

        if resource_ids is None or len(resource_ids) == 0:
            return {
                'type': 'error',
                'message': 'resources_are_invalid',
            }

        result = {}

        for plugin_name in ['opponent', 'input', 'taboo']:
            if query.get(f'{plugin_name}_type') is not None:
                try:
                    result[plugin_name] = list(
                        self.plugins[plugin_name].run(
                            resource_ids,
                            query['game_options'],
                            query[f'{plugin_name}_type'],
                            configs=get_configs(query, plugin_name),
                        )
                    )
                except Exception as error:
                    logger.error(traceback.format_exc())

                    return {
                        'type': 'error',
                        'message': f'{plugin_name}s_are_invalid',
                    }

        game = self.merge_to_game(result, resource_ids)
        
        # logger.info(f'[Game Controller] Game: {game}')

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

            return {
                'type': 'error',
                'message': 'game_options_are_invalid',
            }

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
        def add_params(plugin_type, plugin_options):
            for name, values in plugin_options.items():
                if not isinstance(values, (list, set)):
                    values = [values]

                for value in values:
                    bulk_list.append(
                        GameroundParameter(
                            gameround=gameround,
                            plugin_type=plugin_type,
                            name=str(name),
                            value=str(value),
                        )
                    )

        bulk_list = []

        gameround = Gameround(
            user=user,
            gamesession=gamesession,
            resource_id=resource_id,
        )

        for name in query.get('resource_type', []):
            add_params(name, query['resource_options'])

        for name in query.get('opponent_type', []):
            opponent_type, _ = OpponentType.objects \
                .get_or_create(name=name)
            opponent_type.save()

            gameround.opponent_type = opponent_type
            add_params(name, query['opponent_options'])

        for name in query.get('input_type', []):
            input_type, _ = InputType.objects \
                .get_or_create(name=name)
            input_type.save()

            gameround.input_type = input_type
            add_params(name, query['input_options'])

        for name in query.get('taboo_type', []):
            taboo_type, _ = TabooType.objects \
                .get_or_create(name=name)
            taboo_type.save()

            gameround.taboo_type = taboo_type
            add_params(name, query['taboo_options'])

        gameround.save()

        for name in query.get('suggester_type', []):
            suggester_type, _ = SuggesterType.objects \
                .get_or_create(name=name)

            gameround.suggester_types.add(suggester_type)
            add_params(name, query['suggester_options'])

        for name in query.get('score_type', []):
            score_type, _ = ScoreType.objects \
                .get_or_create(name=name)

            gameround.score_types.add(score_type)
            add_params(name, query['score_options'])

        if bulk_list:
            GameroundParameter.objects.bulk_create(bulk_list)

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

        for config_name, plugin_manager in self.plugins.items():
            config_type = f'{config_name}_type'
            config_options = f'{config_name}_options'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(self._type, config['game_types']):
                        values = query.get(config_type)

                        if values is None:
                            values = query.getlist(f'{config_type}[]')
                            
                        if values is not None:
                            if is_in(config['name'], values):
                                result[config_type].append(config['type'])
                        elif config.get('default', False):
                            result[config_type].append(config['type'])

            if result.get(config_type):
                result[config_options] = {}

                for key, value in query.items():
                    if key.startswith(f'{config_name}_'):
                        if key.endswith('[]'):
                            value = query.getlist(key)
                            key = key.strip()[:-2]

                        key = key.split('_', 1)[-1]

                        if key.lower() != 'type':
                            result[config_options][key] = to_type(value)

        return dict(result)

    def merge_to_game(self, result, resource_ids):
        game = defaultdict(dict)

        resources = Resource.objects \
            .filter(id__in=resource_ids) \
            .values(
                'id',
                'hash_id',
                'collection_id',
            )

        resources = {
            str(x['id']): {
                'resource_id': str(x['id']),
                'path': upload_url_to_image(x['hash_id']) \
                    if x['collection_id'] and settings.IS_DEV \
                    else media_url_to_image(x['hash_id']),
            }
            for x in list(resources)
        }

        if result:
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

        return resources
