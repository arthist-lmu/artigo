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
    resource = ResourcePluginManager(
        configs=config.get('resources', []),
    )
    resource.find('resource')

    opponent = OpponentPluginManager(
        configs=config.get('opponents', []),
    )
    opponent.find('opponent')

    taboo = TabooPluginManager(
        configs=config.get('taboos', []),
    )
    taboo.find('taboo')

    score = ScorePluginManager(
        configs=config.get('scores', []),
    )
    score.find('score')

    data = {
        'resource': resource,
        'opponent': opponent,
        'taboo': taboo,
        'score': score,
    }

    return data
