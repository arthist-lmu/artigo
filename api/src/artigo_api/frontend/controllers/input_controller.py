from collections import defaultdict
from django.forms.models import model_to_dict
from frontend.utils import is_in


class InputController:
    def __init__(
        self,
        filter_plugin_manager=None,
        score_plugin_manager=None,
    ):
        super().__init__()

        self.filter_plugin_manager = filter_plugin_manager
        self.score_plugin_manager = score_plugin_manager

    def parse_query(self, gameround, query):
        result = defaultdict(list)

        result['game_options'] = {
            'resource_id': query.get('resource_id'),
            'language': query.get('language', 'de'),
        }

        if not isinstance(gameround, dict):
            gameround = model_to_dict(gameround)

        plugins = {
            'filter': self.filter_plugin_manager,
        }

        for plugin_name, plugin_manager in plugins.items():
            plugin_type = f'{plugin_name}_type'

            if plugin_manager:
                for plugin in plugin_manager.plugin_list:
                    config = plugin.get('config', {})

                    if is_in(result['game_type'], config['game_types']):
                        parent_name = config['name'].split('_', 1)[0]

                        if config.get('default', False):
                            result[plugin_type].append(config['type'])
                        elif gameround.get(f'{parent_name}_type'):
                            result[plugin_type].append(config['type'])

        for score_type in gameround.get('score_types', []):
            result['score_type'].append(score_type.name)

        return dict(result)
