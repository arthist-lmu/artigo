import copy
import grpc
import time
import uuid
import logging
import traceback

from concurrent import futures
from google.protobuf.json_format import MessageToDict, ParseDict
from . import index_pb2, index_pb2_grpc
from .plugins import *
from .database import *
from .jobs import InsertJob
from .utils import (
    meta_to_proto,
    meta_from_proto,
    tags_to_proto,
    tags_from_proto,
    read_chunk,
)

logger = logging.getLogger(__name__)


def search(args):
    try:
        searcher = Searcher(Backbone(args['config'].get('opensearch')))

        results = searcher(
            ParseDict(args['query'], index_pb2.SearchRequest()),
            limit=args['query'].get('limit', 100),
            offset=args['query'].get('offset', 0),
        )

        result = index_pb2.ListSearchResultReply()
        result.total = results['total']
        result.offset = args['query'].get('offset', 0)

        for e in results.get('entries', []):
            entry = result.entries.add()
            entry.id = e['meta']['id']

            if e.get('hash_id'):
                entry.hash_id = e['hash_id']

            if e.get('metadata'):
                meta_to_proto(entry.meta, e['metadata'])

            if e.get('tags'):
                tags_to_proto(entry.tags, e['tags'])

            if e.get('collection'):
                entry.source.id = e['collection']['id']
                entry.source.name = e['collection']['name']
                entry.source.url = e['collection']['url']
                entry.source.is_public = e['collection']['is_public']

        for a in results.get('aggregations', []):
            aggregation = result.aggregations.add()
            aggregation.field = a['field']

            for e in a['entries']:
                value_field = aggregation.entries.add()
                value_field.key = e['name']
                value_field.int_val = e['value']

        return MessageToDict(result)
    except Exception as error:
        logger.error(traceback.format_exc())

    return None


def init_plugins(config):
    data = {
        'reconciliator': ReconciliatorPluginManager(
            configs=config.get('reconciliators', []),
        ),
    }

    for key, manager in data.items():
        manager.find(key)

    return data


def init_process(config):
    globals().update(init_plugins(config))


class Commune(index_pb2_grpc.IndexServicer):
    def __init__(self, config):
        self.futures = []
        self.config = config
        self.managers = init_plugins(config)

        self.process_pool = futures.ProcessPoolExecutor(
            max_workers=1, initializer=init_process, initargs=(config,)
        )

        self.insert_process_pool = futures.ProcessPoolExecutor(
            max_workers=8, initializer=InsertJob().init_worker, initargs=(config,)
        )

    def status(self, request, context):
        futures_data = {x['id']: i for i, x in enumerate(self.futures)}

        if request.id in futures_data:
            job_data = self.futures[futures_data[request.id]]

            if not job_data['future'].done():
                return index_pb2.StatusReply(status='running')

            result = job_data['future'].result()

            if result is not None:
                return index_pb2.StatusReply(status='done')

        return index_pb2.StatusReply(status='error')

    def get(self, request, context):
        json_obj = MessageToDict(request)
        results = index_pb2.GetReply()

        logger.info(f'[Server] Get: {json_obj}')

        backbone = Backbone(config=self.config.get('opensearch', {}))

        for x in backbone.get(ids=json_obj['ids']):
            entry = results.entries.add()
            entry.id = x['meta']['id']

            if x.get('hash_id'):
                entry.hash_id = x['hash_id']

            if x.get('metadata'):
                meta_to_proto(entry.meta, x['metadata'])

            if x.get('tags'):
                tags_to_proto(entry.tags, x['tags'])

            if x.get('collection'):
                entry.source.id = x['collection']['id']
                entry.source.name = x['collection']['name']
                entry.source.url = x['collection']['url']
                entry.source.is_public = x['collection']['is_public']

        return results

    def insert(self, request, context):
        def translate(cache, request):
            for x in request:
                entry = {
                    'id': x.image.id,
                    'meta': meta_from_proto(x.image.meta),
                    'tags': tags_from_proto(x.image.tags),
                    'cache': cache[x.image.id],
                }

                if x.image.hash_id:
                    entry['hash_id'] = x.image.hash_id

                if x.image.source.id:
                    entry['source'] = {
                        'id': x.image.source.id,
                        'name': x.image.source.name,
                        'url': x.image.source.url,
                        'is_public': x.image.source.is_public,
                    }

                yield entry

        backbone = Backbone(config=self.config.get('opensearch', {}))
        cache_config = self.config.get('cache', {'cache_dir': None})

        request_iter = iter(request)
        db_cache = []

        with Cache(cache_config['cache_dir'], mode='r') as cache:
            while True:
                chunk = read_chunk(translate(cache, request_iter), chunksize=512)

                if len(chunk) <= 0:
                    break

                results = self.insert_process_pool.map(InsertJob(), chunk, chunksize=64)

                for status, entry in results:
                    if status != 'ok':
                        logger.error(f"[Server] Insert: {entry['id']}")
                        yield index_pb2.InsertReply(status='error', id=entry['id'])

                        continue

                    db_cache.append(entry)

                    if len(db_cache) > 64:
                        try_count = 20

                        while try_count > 0:
                            try:
                                backbone.insert(db_cache)

                                db_cache = []
                                try_count = 0
                            except KeyboardInterrupt:
                                raise
                            except Exception as error:
                                logger.error(traceback.format_exc())

                                try_count -= 1
                                time.sleep(1)

                    yield index_pb2.InsertReply(status='ok', id=entry['id'])

        if len(db_cache) > 0:
            backbone.insert(db_cache)
            db_cache = []

    def delete(self, request, context):
        logger.info('[Server] Delete')

        json_obj = MessageToDict(request)

        backbone = Backbone(config=self.config.get('opensearch', {}))
        status = backbone.delete(indices=json_obj['names'])

        return index_pb2.DeleteReply(status=status)

    def search(self, request, context):
        json_obj = MessageToDict(request)
        job_id = uuid.uuid4().hex

        logger.info(f'[Server] Search: {json_obj}')
        
        variable = {
            'id': job_id,
            'query': json_obj,
            'config': self.config,
            'future': None,
        }

        variable['future'] = self.process_pool.submit(
            search, copy.deepcopy(variable),
        )

        self.futures.append(variable)

        return index_pb2.SearchReply(id=job_id)

    def list_search_result(self, request, context):
        futures_data = {x['id']: i for i, x in enumerate(self.futures)}

        if request.id in futures_data:
            job_data = self.futures[futures_data[request.id]]

            if not job_data['future'].done():
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details('Still running')

                return index_pb2.ListSearchResultReply()

            try:
                result = job_data['future'].result()
                result = ParseDict(result, index_pb2.ListSearchResultReply())
            except Exception as error:
                logger.error(f'[Server] Search: {repr(error)}')
                logger.error(traceback.format_exc())

                result = None

            if result is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details('Search error')

                return index_pb2.ListSearchResultReply()

            return result

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Unknown job')

        return index_pb2.ListSearchResultReply()

    def aggregate(self, request, context):
        json_obj = MessageToDict(request)
        result = index_pb2.AggregateReply()

        logger.info(f'[Server] Aggregate: {json_obj}')

        searcher = Searcher(Backbone(self.config.get('opensearch')))
        results = searcher(request, limit=0, offset=0)

        for a in results.get('aggregations', []):
            aggregation = result.aggregations.add()
            aggregation.field = a['field']

            for e in a['entries']:
                value_field = aggregation.entries.add()
                value_field.key = e['name']
                value_field.int_val = e['value']

        return result

    def reconcile(self, request, context):
        json_obj = MessageToDict(request)
        result = index_pb2.ReconcileReply()

        logger.info(f'[Server] Reconcile: {json_obj}')

        reconciliator = self.managers.get('reconciliator')
        size = 5 if request.size <= 0 else request.size

        for x in reconciliator.run(json_obj, size):
            reconciliation = result.reconciliations.add()
            reconciliation.term.name = x['name']
            reconciliation.term.type = x['type']
            reconciliation.service = x['service']

            if x.get('ids'):
                reconciliation.term.ids.extend(x['ids'])

            for e in x['entries']:
                entry = reconciliation.entries.add()
                entry.id = e['id']
                entry.name = e['name']
                entry.score = e['score']

                if e.get('description'):
                    entry.description = e['description']

        return result


class Server:
    def __init__(self, config):
        self.config = config
        self.commune = Commune(config)

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),
                ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ],
        )

        index_pb2_grpc.add_IndexServicer_to_server(
            self.commune, self.server,
        )

        port = config.get('grpc', {}).get('port', 50051)
        self.server.add_insecure_port(f'[::]:{port}')

    def run(self):
        self.server.start()
        logger.info('[Server] Ready')

        try:
            while True:
                n_jobs = len(self.commune.futures)
                logger.info(f'[Server] Number of jobs: {n_jobs}')
                time.sleep(1000)
        except KeyboardInterrupt:
            self.server.stop(0)
