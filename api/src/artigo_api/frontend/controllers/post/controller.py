import logging

from collections import defaultdict
from django.forms.models import model_to_dict
from frontend import cache as frontend_cache
from frontend.utils import is_in

logger = logging.getLogger(__name__)


class InputController:
    def __init__(self):
        super().__init__()

        self.plugins = frontend_cache.plugins()

    def parse_query(self, gameround, query):
        result = defaultdict(list)

        result['game_options'] = {
            'resource_id': query.get('resource_id'),
            'language': query.get('game_language', 'de'),
        }

        if query.get('tag'):
            if not isinstance(query['tag'], (list, set)):
                query['tag'] = [query['tag']]

            for tag in query['tag']:
                if not isinstance(tag, dict):
                    tag = {'name': tag}

                if not tag.get('suggested'):
                    tag['suggested'] = False

                tag['name'] = tag['name'].lower()
                tag['valid'] = True
                tag['score'] = 0

                result['tags'].append(tag)

        if not isinstance(gameround, dict):
            # TODO: change handling of model_to_dict
            gameround = model_to_dict(gameround)

        for config_name, plugin_manager in self.plugins.items():
            config_type = f'{config_name}_type'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(self._type, config['game_types']):
                        parent_name = config['name'].split('_', 1)[0]

                        if config.get('default', False):
                            result[config_type].append(config['type'])
                        elif gameround.get(f'{parent_name}_type'):
                            result[config_type].append(config['type'])

                        for child in gameround.get(f'{config_type}s', []):
                            if child.name == config['type']:
                                result[config_type].append(child.name)

        return dict(result)
