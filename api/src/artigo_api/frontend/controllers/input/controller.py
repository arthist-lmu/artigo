from collections import defaultdict
from django.core.cache import cache
from django.forms.models import model_to_dict
from frontend.utils import is_in


class InputController:
    def __init__(self):
        super().__init__()

        self.plugins = cache.get('plugins', {})

    def parse_query(self, gameround, query):
        result = defaultdict(list)

        result['game_options'] = {
            'resource_id': query.get('resource_id'),
            'language': query.get('language', 'de'),
        }

        if query.get('tag'):
            if not isinstance(query['tag'], (list, set)):
                query['tag'] = [query['tag']]

            for tag in query['tag']:
                if not isinstance(tag, dict):
                    tag = {'name': tag}

                tag['name'] = tag['name'].lower()
                tag['valid'] = True
                tag['score'] = 0

                result['tags'].append(tag)

        if not isinstance(gameround, dict):
            gameround = model_to_dict(gameround)

        for plugin_name, plugin_manager in self.plugins.items():
            plugin_type = f'{plugin_name}_type'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(self._type, config['game_types']):
                        parent_name = config['name'].split('_', 1)[0]

                        if config.get('default', False):
                            result[plugin_type].append(config['type'])
                        elif gameround.get(f'{parent_name}_type'):
                            result[plugin_type].append(config['type'])

        for score_type in gameround.get('score_types', []):
            result['score_type'].append(score_type.name)

        return dict(result)
