import copy
import grpc
import time
import uuid
import logging
import traceback

from concurrent import futures
from google.protobuf.json_format import MessageToJson, MessageToDict, ParseDict
from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.plugins.cache import Cache
from artigo_search.database.backbone import Backbone
from artigo_search.database.aggregator import Aggregator
from artigo_search.jobs import InsertJob
from artigo_search.utils import meta_to_proto, tags_to_proto
from artigo_search.utils import meta_from_proto, tags_from_proto, read_chunk

logger = logging.getLogger(__name__)


def search(args):
    try:
        pass
    except Exception as error:
        logger.error(f'[Server] Search: {repr(error)}')
        logger.error(traceback.format_exc())

    return None


def init_plugins(config):
    data = {}

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
        
        self.max_results = config.get('index', {}).get('max_results', 100)

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
        logger.info('[Server] Start get')

        json_obj = MessageToDict(request)
        results = index_pb2.GetReply()

        backbone = Backbone(config=self.config.get('opensearch', {}))

        for x in backbone.get(hash_ids=json_obj['ids']):
            entry = results.entries.add()
            entry.id = x['id']

            if x.get('meta'):
                meta_to_proto(entry.meta, x['meta'])

            if x.get('source'):
                entry.source.id = x['source']['id']
                entry.source.name = x['source']['name']
                entry.source.url = x['source']['url']
                entry.source.is_public = x['source']['is_public']

            if x.get('tags'):
                tags_to_proto(entry.tags, x['tags'])

        return results

    def insert(self, request, context):
        def translate(cache, request):
            for x in request:
                source = {}

                if x.image.source.id:
                    source['id'] = x.image.source.id
                    source['name'] = x.image.source.name
                    source['url'] = x.image.source.url
                    source['is_public'] = x.image.source.is_public

                yield {
                    'id': x.image.id,
                    'meta': meta_from_proto(x.image.meta),
                    'source': source,
                    'tags': tags_from_proto(x.image.tags),
                    'cache': cache[x.image.id],
                }

        logger.info('[Server] Start insert')

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

                for i, (status, entry) in enumerate(results):
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
                                try_count -= 1
                                time.sleep(1)

                    yield index_pb2.InsertReply(status='ok', id=entry['id'])

        if len(db_cache) > 0:
            backbone.insert(db_cache)
            db_cache = []

    def delete(self, request, context):
        logger.info('[Server] Start delete')

        json_obj = MessageToDict(request)

        backbone = Backbone(config=self.config.get('opensearch', {}))
        status = backbone.delete(indices=json_obj['names'])

        return index_pb2.DeleteReply(status=status)

    def search(self, request, context):
        logger.info('[Server] Start search')

        json_obj = MessageToDict(request)
        job_id = uuid.uuid4().hex
        
        variable = {
            'id': job_id,
            'query': json_obj,
            'config': self.config,
            'future': None,
        }

        variable['future'] = self.process_pool.submit(
            search, copy.deepcopy(variable)
        )

        self.futures.append(variable)

        return index_pb2.SearchReply(id=job_id)

    def aggregate(self, request, context):
        backbone = Backbone(config=self.config.get('opensearch', {}))
        aggregator = Aggregator(backbone)

        # TODO

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

                n_jobs_done = len([
                    x for x in self.commune.futures
                    if x['future'].done()
                ])

                logger.info(f'[Server] Jobs: {n_jobs_done}/{n_jobs}')

                time.sleep(10)
        except KeyboardInterrupt:
            self.server.stop(0)
