import grpc
import logging
import traceback

from .utils import ResourceViewHelper
from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ParseError,
    NotFound,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from frontend.utils import media_url_to_image

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto, tags_from_proto

logger = logging.getLogger(__name__)


@extend_schema(methods=['POST'], exclude=True)
class ResourceView(ResourceViewHelper):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                description='Resource identifier',
                name='id',
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
        params = request.query_params

        if not params.get('id'):
            raise ParseError('resource_id_required')

        result = self.rpc_get(params, multiple=False)

        if result is None:
            raise NotFound('unknown_resource')
        
        return Response(result)
