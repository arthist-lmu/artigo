import logging

from collections import defaultdict
from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class ScorePlugin(Plugin):
    _type = 'score'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tag_names, gameround, params):
        return self.call(tag_names, gameround, params)


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

    def run(self, tag_names, gameround, params, plugins=None, configs=None):
        results = defaultdict(int)

        if not isinstance(tag_names, list):
            tag_names = [tag_names]

        tag_names = [x.lower() for x in tag_names]

        for plugin in self.plugin_list:
            for entry in plugin['plugin'](tag_names, gameround, params):
                if isinstance(entry, dict):
                    results[entry['name']] += entry['score']

        results = [{'name': k, 'score': v} for k, v in results.items()]

        return results
