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
    data = {
        'resource': ResourcePluginManager(
            configs=config.get('resources', []),
        ),
        'opponent': OpponentPluginManager(
            configs=config.get('opponents', []),
        ),
        'taboo': TabooPluginManager(
            configs=config.get('taboos', []),
        ),
        'suggester': SuggesterPluginManager(
            configs=config.get('suggesters', []),
        ),
        'filter': FilterPluginManager(
            configs=config.get('filters', []),
        ),
        'score': ScorePluginManager(
            configs=config.get('scores', []),
        ),
    }

    for key, manager in data.items():
        manager.find(key)

    return data
