import logging

from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class ScorePlugin(Plugin):
    _type = 'score'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tags, gameround, params):
        return self.call(tags, gameround, params)


class ScorePluginManager(PluginManager):
    _score_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('score')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._score_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._score_plugins

    def run(self, tags, gameround, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        for plugin in plugin_list:
            for entry in plugin['plugin'](tags.keys(), gameround, params):
                if 'score' not in tags[entry['name']]:
                    tags[entry['name']]['score'] = 0
                    
                tags[entry['name']]['score'] += entry['score']

        return tags
