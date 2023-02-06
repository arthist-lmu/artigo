import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils.timezone import make_aware
from .plugin import Plugin
from .manager import PluginManager

logger = logging.getLogger(__name__)


class ResourcePlugin(Plugin):
    _type = 'resource'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, params):
        return self.call(params)

    def exclude_last_played(self, resources, params):
        if params.get('user_id') and self.max_last_played > 0:
            max_last_played = make_aware(datetime.today()) \
                - relativedelta(days=self.max_last_played)

            user_resources = self.model.objects \
                .filter(
                    user_id=params['user_id'],
                    created__gt=max_last_played
                ) \
                .values('resource')

            resources = resources.exclude(id__in=user_resources)

        return resources

    def filter_collections(self, resources, params):
        query = Q(collection__isnull=True)
        query |= Q(collection__access='O')

        if params.get('user_id'):
            query |= Q(collection__user_id=params['user_id'])

        return resources.filter(query)


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
