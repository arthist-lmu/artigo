import logging

from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class ResourcePlugin(Plugin):
    _type = 'resource'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, params):
        return self.call(params)


class ResourcePluginManager(PluginManager):
    _resource_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('resource')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._resource_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._resource_plugins

    def run(self, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        if len(plugin_list) > 1:
            logger.error('Only one resource plugin is permitted.')
            raise ValueError

        results = []

        for plugin in plugin_list:
            for entry in plugin['plugin'](params):
                results.append(entry)

        return results
