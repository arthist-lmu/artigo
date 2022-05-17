import logging

from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('RandomROIResource')
class RandomROIResource(ResourcePlugin):
    default_config = {
        'rounds': 5,
        'max_last_played': 6 * 30,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rounds = self.config['rounds']
        self.max_last_played = self.config['max_last_played']

    def __call__(self, params):
        pass
