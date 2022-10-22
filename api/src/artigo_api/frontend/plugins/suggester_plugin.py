import logging

from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class SuggesterPlugin(Plugin):
    _type = 'suggester'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tags, params):
        return self.call(tags, params)


class SuggesterPluginManager(PluginManager):
    _suggester_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('suggester')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._suggester_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._suggester_plugins

    def run(self, tags, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        for plugin in plugin_list:
            # modify tags in-place in the respective plugin
            plugin['plugin'](tags, params)

        return tags
