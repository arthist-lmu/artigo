import os
import copy
import grpc
import json
import time
import logging

from . import index_pb2, index_pb2_grpc

logger = logging.getLogger(__name__)


def get_latest_dump(dump_folder, raw=False):
    dump_files = []

    for file in sorted(
        os.scandir(dump_folder),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    ):
        suffix = '-raw' if raw else ''

        if file.name.startswith(f'os-dump{suffix}_'):
            dump_files.append(file.name)

    return os.path.join(dump_folder, dump_files[0])


def extract_from_jsonl(file_path, media_folder):
    entries = []

    base_fields = {
        'id',
        'hash_id',
        'meta',
        'tags',
        'source',
    }

    with open(file_path, 'r', encoding='utf-8') as file_obj:
        for line in file_obj:
            entry = json.loads(line)
            entry['id'] = str(entry['id'])

            if not entry.get('meta'):
                entry['meta'] = {}

            for field, value in copy.deepcopy(entry).items():
                if field not in base_fields and value:
                    entry['meta'][field] = value

            entries.append(entry)

    return entries


class Client:
    def __init__(self, config=None):
        if config is None:
            config = {}

        if 'grpc' not in config:
            config['grpc'] = {}

        host = config['grpc'].get('host', 'localhost')
        port = config['grpc'].get('port', 50051)

        self.channel = grpc.intercept_channel(
            grpc.insecure_channel(
                f'{host}:{port}',
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

    def count(self):
        request = index_pb2.CountRequest()

        return self.stub.count(request)

    def get(self, params):
        request = index_pb2.GetRequest()

        if isinstance(params['id'], (list, set)):
            request.ids.extend(map(str, params['id']))
        else:
            request.ids.extend([str(params['id'])])

        return self.stub.get(request)

    def insert(self):
        def entry_generator(entries, blacklist):
            for entry in entries:
                if blacklist and entry['id'] in blacklist:
                    continue

                request = index_pb2.InsertRequest()

                request_image = request.image
                request_image.id = entry['id']
                request_image.hash_id = entry['hash_id']

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
                            tag_field.language = tag['language']
                            tag_field.count = tag['count']

                yield request

        file_path = get_latest_dump('/dump', raw=False)
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

    def delete(self):
        request = index_pb2.DeleteRequest()

        return self.stub.delete(request)
