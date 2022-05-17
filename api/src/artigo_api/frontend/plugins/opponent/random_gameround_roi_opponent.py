import logging

from frontend.plugins import (
    OpponentPlugin,
    OpponentPluginManager,
)

logger = logging.getLogger(__name__)


@OpponentPluginManager.export('RandomGameroundROIOpponent')
class RandomGameroundTaggingOpponent(OpponentPlugin):
    default_config = {}
    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, resource_ids, params):
        pass
