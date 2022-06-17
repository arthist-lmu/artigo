import logging

from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class InputPlugin(Plugin):
    _type = 'input'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, resource_ids, params):
        return self.call(resource_ids, params)


class InputPluginManager(PluginManager):
    _input_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('input')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._input_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._input_plugins

    def run(self, resource_ids, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        if len(plugin_list) > 1:
            logger.error('Only one input plugin is permitted.')
            raise ValueError

        results = []

        for plugin in plugin_list:
            for entry in plugin['plugin'](resource_ids, params):
                results.append(entry)

        return results
