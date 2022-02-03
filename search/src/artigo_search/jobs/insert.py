import logging

logger = logging.getLogger(__name__)


class InsertJob:
    def __init__(self, config=None):
        if config is not None:
            self.init_worker(config)

    @classmethod
    def init_worker(cls, config):
        pass

    @classmethod
    def __call__(cls, entry):
        doc = {
            'id': entry['id'], 
            'meta': entry['meta'],
            'tags': entry['tags'],
            'source': entry['source'],
        }

        return 'ok', doc
