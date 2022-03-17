import os
import json
import logging

from .plugins import *
from django.apps import AppConfig
from django.core.cache import cache

logger = logging.getLogger(__name__)


class FrontendConfig(AppConfig):
    name = 'frontend'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            logger.info('[Server] Initialize plugins')
            
            plugins = init_plugins(read_config('/config.json'))
            cache.set('plugins', plugins, timeout=None)


def read_config(file_path):
    with open(file_path, 'r') as file_obj:
        return json.load(file_obj)

    return {}


def init_plugins(config):
    _resource = ResourcePluginManager(
        configs=config.get('resources', []),
    )
    _resource.find('resource')

    _opponent = OpponentPluginManager(
        configs=config.get('opponents', []),
    )
    _opponent.find('opponent')

    _taboo = TabooPluginManager(
        configs=config.get('taboos', []),
    )
    _taboo.find('taboo')

    _filter = FilterPluginManager(
        configs=config.get('filters', []),
    )
    _filter.find('filter')

    _score = ScorePluginManager(
        configs=config.get('scores', []),
    )
    _score.find('score')

    data = {
        'resource': _resource,
        'opponent': _opponent,
        'taboo': _taboo,
        'filter': _filter,
        'score': _score,
    }

    return data
