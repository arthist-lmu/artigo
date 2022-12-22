import json
import logging

from .plugins import *
from .utils import name

logger = logging.getLogger(__name__)


@name
def plugins(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None or kwargs.get('renew'):
        with open(file_path, 'r') as file_obj:
            config = json.load(file_obj)

        values = {
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

        timeout = kwargs.get('timeout', None)
        cache.set(kwargs['name'], values, timeout)

    return values
