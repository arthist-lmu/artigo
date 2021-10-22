import logging

from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

logger = logging.getLogger(__name__)


class Backbone:
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 9200)

        self.client = OpenSearch(
            [{'host': self.host, 'port': self.port}],
            http_compress=True, ssl_show_warn=False,
            use_ssl=False, ssl_assert_hostname=False, 
        )

        self.index = config.get('index', 'artigo')
        self.type = config.get('type', '_doc')

        if not self.client.indices.exists(index=self.index):
            body = {
                'mappings': {
                    'properties': {
                        'id': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256
                                }
                            }
                        },
                        'path': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256
                                }
                            }
                        },
                        'meta': {
                            'type': 'nested',
                            'properties': {
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                },
                                'value_str': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    },
                                    'copy_to': ['all_text']
                                },
                                'value_int': {
                                    'type': 'long'
                                },
                                'value_float': {
                                    'type': 'float'
                                }
                            }
                        },
                        'tags': {
                            'type': 'nested',
                            'properties': {
                                'id': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                },
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    },
                                    'copy_to': ['all_text']
                                },
                                'count': {
                                    'type': 'long'
                                }
                            }
                        },
                        'source': {
                            'type': 'nested',
                            'properties': {
                                'id': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                },
                                'name': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                },
                                'url': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword',
                                            'ignore_above': 256
                                        }
                                    }
                                },
                                'is_public': {
                                    'type': 'boolean'
                                }
                            }
                        },
                        'all_text': {
                            'type': 'text'
                        }
                    }
                }
            }

            self.client.indices.create(index=self.index, body=body)

    def status(self):
        return 'ok' if self.client.ping() else 'error'

    def get(self, hash_ids):
        pass

    def insert(self, generator):
        def add_fields(generator):
            for x in generator:
                logger.info(f"Insert: {x['id']} into {self.index}")
                yield {'_id': x['id'], '_index': self.index, **x}

        bulk(client=self.client, actions=add_fields(generator))

    def delete(self, indices):
        for index in indices:
            self.client.indices.delete(index=index, ignore=[400])

    def search(self, size=100):
        if not self.client.indices.exists(index=self.index):
            return []

        try:
            results = self.client.search(index=self.index, body=body, size=size)

            for x in results['hits']['hits']:
                yield x['_source']
        except exceptions.NotFoundError:
            return []
