import grpc

from rest_framework.views import APIView
from frontend.utils import media_url_to_image, channel

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto


class RPCView(APIView):
    channel = channel()


class ResourceViewHelper(RPCView):
    @staticmethod
    def parse_request(params):
        grpc_request = index_pb2.GetRequest()

        if params.get('id'):
            grpc_request.ids.extend([params['id']])

        if params.get('ids'):
            grpc_request.ids.extend(params['ids'])

        return grpc_request

    def rpc_get(self, params, multiple=True):
        grpc_request = self.parse_request(params)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.get(grpc_request)

            entries = {}

            for x in response.entries:
                entry = {'meta': meta_from_proto(x.meta)}

                if multiple:
                    entry['resource_id'] = x.id
                else:
                    entry['id'] = x.id

                if x.hash_id:
                    entry['path'] = media_url_to_image(x.hash_id)

                if x.source.id:
                    entry['source'] = {
                        'name': x.source.name,
                        'url': x.source.url,
                        'is_public': x.source.is_public,
                    }

                entries[x.id] = entry

            if multiple:
                return entries

            return list(entries.values())[0]
        except grpc.RpcError as error:
            return {}
        