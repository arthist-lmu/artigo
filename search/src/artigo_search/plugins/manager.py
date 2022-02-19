import logging

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, configs=None):
        self.configs = configs

        if configs is None:
            self.configs = []

    def plugins(self):
        return {}

    def init_plugins(self, plugins=None, configs=None):
        if plugins is None:
            plugins = list(self.plugins().keys())

        plugin_names = [x.lower() for x in plugins]

        if configs is None:
            configs = self.configs

        plugin_list = []
        
        for plugin_name, wrapper in self.plugins().items():
            if plugin_name.lower() not in plugin_names:
                continue

            plugin_has_config = False
            plugin_config = {'params': {}}

            for x in configs:
                if x['type'].lower() == plugin_name.lower():
                    plugin_config.update(x)

                    if not x.get('disabled', False):
                        plugin_has_config = True

            if not plugin_has_config:
                continue

            plugin_list.append({
                'plugin': wrapper(config=plugin_config['params']),
                'config': plugin_config,
            })

        return plugin_list
