import os
import re
import json
import logging

from .harvester_plugin import HarvesterPlugin
from .manager import PluginManager
from typing import Generator
from importlib import import_module
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class ReconciliatorPlugin(HarvesterPlugin):
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

        self.find()
        self.plugin_list = self.init_plugins()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._reconciliator_plugins[name] = plugin

            return plugin

        return export_helper

    def plugins(self):
        return self._reconciliator_plugins

    def find(self, path=None):
        if path is None:
            dir_path = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(dir_path, 'reconciliator')

        file_regex = re.compile(r'(.+?)\.py$')

        for file_path in os.listdir(path):
            match = re.match(file_regex, file_path)

            if match is not None:
                module_name = 'artigo_search.plugins.reconciliator.{}'
                x = import_module(module_name.format(match.group(1)))

                if 'register' in dir(x):
                    x.register(self)

    def run(self, queries, size=100):
        results = []

        for plugin in self.plugin_list:
            for entry in plugin['plugin'](queries, size=size):
                results.append(entry)

        return results
