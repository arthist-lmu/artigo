import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import make_aware
from frontend.models import UserROI
from frontend.plugins import (
    ResourcePlugin,
    ResourcePluginManager,
)

logger = logging.getLogger(__name__)


@ResourcePluginManager.export('RandomROIResource')
class RandomROIResource(ResourcePlugin):
    default_config = {
        'rounds': 5,
        'min_rois': 5,
        'max_last_played': 6 * 30,
    }

    default_version = '0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rounds = self.config['rounds']
        self.min_rois = self.config['min_rois']
        self.max_last_played = self.config['max_last_played']

    def __call__(self, params):
        if params.get('id'):
            if not isinstance(params['id'], (list, set)):
                params['id'] = [params['id']]

            # TODO
        else:
            # TODO
            pass

        # TODO

        resources = resources.order_by('?')[:max(1, self.rounds)]

        return resources.values_list('resource_id', flat=True)
