import json
import logging

from .harvester_helper import HarvesterHelper
from .manager import PluginManager
from typing import Generator
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class ReconciliatorPlugin(HarvesterHelper):
    _type = 'reconciliator'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, queries, size=100):
        return self.call(queries, size)

    @staticmethod
    def parse_url(url, params):
        if isinstance(params, Generator):
            params = list(params)
        elif not isinstance(params, (set, list)):
            params = [params]
            
        for p in params:
            p = {k: json.dumps(v) for k, v in p.items()}

            yield f'{url}?{urlencode(p)}'


class ReconciliatorPluginManager(PluginManager):
    _reconciliator_plugins = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.find('reconciliator')
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._reconciliator_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._reconciliator_plugins

    def run(self, queries, size=100, plugins=None, configs=None):
        plugin_list = self.init_plugins(plugins, configs)

        if len(plugin_list) > 1:
            logger.error('Only one reconciliator plugin is permitted.')
            raise ValueError

        results = []

        for plugin in plugin_list:
            for entry in plugin['plugin'](queries, size=size):
                results.append(entry)

        return results
