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

    def run(self, resources, params, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        tags = {}

        for resource in resources:
            for tag in resource['tags']:
                tags[tag['name'].lower()] = set()

        for plugin in plugin_list:
            for entry in plugin['plugin'](tags, params):
                tags[entry['name']].add(entry['suggest'])

        for resource in resources:
            invalid_tags = set(x['name'] for x in resource['tags'])

            for tag in resource['tags']:
                tag['suggest'] = tags[tag['name'].lower()] - invalid_tags

        return resources
