import logging

from .harvester_helper import HarvesterHelper
from .manager import PluginManager

logger = logging.getLogger(__name__)


class DownloaderPlugin(HarvesterHelper):
    _type = 'downloader'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, queries):
        return self.call(queries)


class DownloaderPluginManager(PluginManager):
    _downloader_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('downloader')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._downloader_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._downloader_plugins

    def run(self, queries, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        if len(plugin_list) > 1:
            logger.error('Only one downloader plugin is permitted.')
            raise ValueError

        results = []

        for plugin in plugin_list:
            for entry in plugin['plugin'](queries):
                results.append(entry)

        return results
