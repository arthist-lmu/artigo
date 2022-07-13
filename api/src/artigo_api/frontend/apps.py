import os
import json

from .plugins import *
from django.apps import AppConfig
from django.core.cache import cache


class FrontendConfig(AppConfig):
    name = 'frontend'

    def ready(self):
        plugins = init_plugins(read_config('/config.json'))
        cache.set('plugins', plugins, timeout=None)


def read_config(file_path):
    with open(file_path, 'r') as file_obj:
        return json.load(file_obj)


def init_plugins(config):
    data = {
        'resource': ResourcePluginManager(
            configs=config.get('resources', []),
        ),
        'opponent': OpponentPluginManager(
            configs=config.get('opponents', []),
        ),
        'input': InputPluginManager(
            configs=config.get('inputs', []),
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

    return data
