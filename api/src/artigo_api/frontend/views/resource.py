import grpc
import hashlib
import msgpack
import logging
import traceback

from .utils import RPCView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.utils import media_url_to_image

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto, tags_from_proto

logger = logging.getLogger(__name__)


@extend_schema(methods=['POST'], exclude=True)
class Resource(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.GetRequest()

        if params.get('id'):
            grpc_request.ids.extend([params.get('id')])

        return grpc_request

    def rpc_get(self, params):
        grpc_request = self.parse_request(params)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.get(grpc_request)

            for x in response.entries:
                return {
                    'id': x.id,
                    'meta': meta_from_proto(x.meta),
                    'tags': tags_from_proto(x.tags),
                    'path': media_url_to_image(x.id),
                    'source': {
                        'id': x.source.id,
                        'name': x.source.name,
                        'url': x.source.url,
                        'is_public': x.source.is_public,
                    },
                }
        except grpc.RpcError as error:
            pass

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                description='Resource identifier',
                required=True,
                type=str,
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'id': {
                        'description': 'Resource identifier',
                        'type': 'string',
                    },
                    'meta': {
                        'description': 'Metadata',
                        'type': 'array',
                        'items': {
                            'properties': {
                                'name': {
                                    'description': 'Name of field',
                                    'type': 'string',
                                    'enum': [
                                        'titles',
                                        'creators',
                                        'location',
                                        'institution',
                                    ],
                                },
                                'value_str': {
                                    'description': 'String value of field',
                                    'type': 'string',
                                },
                            },
                        },
                    },
                    'tags': {
                        'description': 'Crowd-generated tags',
                        'type': 'array',
                        'items': {
                            'properties': {
                                'id': {
                                    'description': 'Tag identifier',
                                    'type': 'string',
                                },
                                'name': {
                                    'description': 'Name of tag',
                                    'type': 'string',
                                },
                                'language': {
                                    'description': 'Language of tag',
                                    'type': 'string',
                                },
                                'count': {
                                    'description': 'Number of taggings',
                                    'type': 'integer',
                                },
                            },
                        },
                    },
                    'path': {
                        'description': 'File path to resource image',
                        'type': 'string',
                    },
                    'source': {
                        'description': 'Source information',
                        'type': 'object',
                        'properties': {
                            'id': {
                                'description': 'Source identifier',
                                'type': 'string',
                            },
                            'name': {
                                'description': 'Name of source',
                                'type': 'string',
                            },
                            'url': {
                                'description': 'URL of source',
                                'type': 'string',
                            },
                            'is_public': {
                                'description': 'Publicly visible?',
                                'type': 'boolean',
                            },
                        },
                    },
                },
            },
        },
        description='Retrieve metadata and crowd-generated tags of a resource.',
    )
    def get(self, request, format=None):
        result = self.rpc_get(request.query_params)

        if result is None:
            raise APIException('unknown_resource')
        
        return Response(result)

    def post(self, request, format=None):
        logger.debug("Process post")
        imgID = request.POST.get("imgID")
        tag = request.POST.get("tag")

        already_tagged = True
        if already_tagged:
            performance = {
                "points": 5
            }
            return Response(performance)

        raise APIException('unknown_resource')
