import grpc
import time
import uuid
import pytest

from .. import index_pb2, index_pb2_grpc


def request_insert():
    def entries():
        for entry in [
            {
                'creators': 'Adolph Menzel',
                'titles': 'Das Eisenwalzwerk',
            }
        ]:
            request = index_pb2.InsertRequest()

            request_image = request.image
            request_image.id = uuid.uuid4().hex

            for field, value in entry.items():
                meta_field = request_image.meta.add()
                meta_field.key = field
                meta_field.string_val = value

            yield request

    channel = grpc.insecure_channel('localhost:50051')
    stub = index_pb2_grpc.IndexStub(channel)

    return stub.insert(entries())


def test_response():
    request_iter = iter(request_insert())
    try_count = 5

    while try_count > 0:
        for entry in request_iter:
            if entry.status == 'ok':
                try_count = 0
                break

            try_count -= 1
            time.sleep(1)

    assert entry.status == 'ok'
