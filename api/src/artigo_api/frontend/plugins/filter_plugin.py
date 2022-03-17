import logging

from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class FilterPlugin(Plugin):
    _type = 'filter'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, tags, gameround, params):
        return self.call(tags, gameround, params)


class FilterPluginManager(PluginManager):
    _filter_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('filter')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._filter_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._filter_plugins

    def run(self, tags, gameround, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        if not isinstance(tags, (list, set)):
            tags = [tags]

        tags = [x.lower() for x in tags]
        results = dict.fromkeys(tags, True)

        for plugin in plugin_list:
            for entry in plugin['plugin'](tags, gameround, params):
                if isinstance(entry, dict):
                    if not entry.get('valid', True):
                        results[entry['name']] = False

        results = [k for k, v in results.items() if v]

        return results
