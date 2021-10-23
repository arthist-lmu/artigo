import os
import copy
import grpc
import json
import time
import logging

from artigo_search import index_pb2, index_pb2_grpc

logger = logging.getLogger(__name__)


def get_latest_dump(dump_folder):
    dump_paths = []

    for file_path in os.listdir(dump_folder):
        if file_path.startswith('os-dump'):
            dump_paths.append(file_path)

    if dump_paths:
        latest_dump = sorted(dump_paths)[-1]

        return os.path.join(dump_folder, latest_dump)


def extract_from_jsonl(file_path, media_folder):
    entries = []

    base_fields = {
        'id', 'hash_id', 'meta', 
        'tags', 'source',
    }

    with open(file_path, 'r', encoding='utf-8') as file_obj:
        for line in file_obj:
            entry = json.loads(line)

            if entry.get('hash_id'):
                entry['id'] = entry['hash_id']

            entry['id'] = str(entry['id'])

            if not entry.get('meta'):
                entry['meta'] = {}

            for field, value in copy.deepcopy(entry).items():
                if field not in base_fields:
                    entry['meta'][field] = value

            entries.append(entry)

    return entries


class Client:
    def __init__(self, config):
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 50051)

        self.channel = grpc.intercept_channel(
            grpc.insecure_channel(
                f'{self.host}:{self.port}',
                options=[
                    ('grpc.max_send_message_length', 50 * 1024 * 1024),
                    ('grpc.max_receive_message_length', 50 * 1024 * 1024),
                    ('grpc.keepalive_time_ms', 2 ** 31 - 1),
                ],
            ),
        )

        self.stub = index_pb2_grpc.IndexStub(self.channel)

    def status(self, job_id):
        request = index_pb2.StatusRequest()
        request.id = job_id

        return self.stub.status(request)

    def get(self, params):
        request = index_pb2.GetRequest()

        if isinstance(params['hash_id'], (list, set)):
            request.ids.extend(map(str, params['hash_id']))
        else:
            request.ids.extend([str(params['hash_id'])])

        return self.stub.get(request)

    def insert(self):
        def entry_generator(entries, blacklist):
            for entry in entries:
                if blacklist and entry['id'] in blacklist:
                    continue

                request = index_pb2.InsertRequest()

                request_image = request.image
                request_image.id = entry['id']

                if entry.get('meta'):
                    for field, values in entry['meta'].items():
                        if isinstance(values, (list, set)):
                            for value in values:
                                meta_field = request_image.meta.add()
                                meta_field.key = field

                                if isinstance(value, dict):
                                    if value.get('name'):
                                        meta_field.string_val = value['name']
                                elif isinstance(value, (str, int, float)):
                                    if isinstance(value, str):
                                        meta_field.string_val = value
                                    elif isinstance(value, int):
                                        meta_field.int_val = value
                                    elif isinstance(value, float):
                                        meta_field.float_val = value
                        elif isinstance(values, (str, int, float)):
                            meta_field = request_image.meta.add()
                            meta_field.key = field

                            if isinstance(values, str):
                                meta_field.string_val = values
                            elif isinstance(values, int):
                                meta_field.int_val = values
                            elif isinstance(values, float):
                                meta_field.float_val = values

                if entry.get('source'):
                    if isinstance(entry['source'], dict):
                        source_field = request_image.source

                        if entry['source'].get('id'):
                            source_field.id = str(entry['source']['id'])

                        if entry['source'].get('name'):
                            source_field.name = entry['source']['name']

                        if entry['source'].get('url'):
                            source_field.url = entry['source']['url']

                if entry.get('tags'):
                    if isinstance(entry['tags'], (list, set)):
                        for tag in entry['tags']:
                            tag_field = request_image.tags.add()

                            tag_field.id = str(tag['id'])
                            tag_field.name = tag['name']
                            tag_field.count = tag['count']
                            tag_field.language = tag['language']

                yield request

        file_path = get_latest_dump('/dump')
        entries = extract_from_jsonl(file_path, '/media')

        blacklist = set()
        try_count = 20

        while try_count > 0:
            try:
                gen_iter = entry_generator(entries, blacklist)

                for entry in self.stub.insert(gen_iter):
                    blacklist.add(entry.id)

                try_count = 0
            except KeyboardInterrupt:
                raise
            except Exception as error:
                logger.error(error)
                try_count -= 1

    def delete(self, params):
        request = index_pb2.DeleteRequest()

        if isinstance(params['name'], (list, set)):
            request.names.extend(map(str, params['name']))
        else:
            request.names.extend([str(params['name'])])

        return self.stub.delete(request)

    def search(self, params):
        request = index_pb2.SearchRequest()

        for query in params['query']:
            term_field = request.terms.add()
            term_field.text.query = query['value']
            term_field.text.flag = query['flag']

            if query.get('field'):
                if not isinstance(query['field'], str):
                    continue

                term_field.text.field = query['field']

        response = self.stub.search(request)
        request = index_pb2.ListSearchResultRequest(id=response.id)

        for x in range(500):
            try:
                return stub.list_search_result(request)
            except grpc.RpcError as error:
                if error.code() == grpc.StatusCode.FAILED_PRECONDITION:
                    time.sleep(0.01)  # search is still running

        return {'status': 'error', 'job_id': response.id}
