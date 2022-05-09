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
        }

        if entry.get('source'):
            doc['source'] = entry['source']

        if entry.get('hash_id'):
            doc['hash_id'] = entry['hash_id']

        return 'ok', doc
