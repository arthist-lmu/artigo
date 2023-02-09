import json
import logging

from django.core.cache import cache
from frontend.plugins import *
from .utils import name

logger = logging.getLogger(__name__)


@name
def plugins(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        with open('/config.json', 'r') as file_obj:
            config = json.load(file_obj)

        values = {
            'resource': ResourcePluginManager(
                configs=config.get('resource', []),
            ),
            'opponent': OpponentPluginManager(
                configs=config.get('opponent', []),
            ),
            'input': InputPluginManager(
                configs=config.get('input', []),
            ),
            'taboo': TabooPluginManager(
                configs=config.get('taboo', []),
            ),
            'suggester': SuggesterPluginManager(
                configs=config.get('suggester', []),
            ),
            'filter': FilterPluginManager(
                configs=config.get('filter', []),
            ),
            'score': ScorePluginManager(
                configs=config.get('score', []),
            ),
        }

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
