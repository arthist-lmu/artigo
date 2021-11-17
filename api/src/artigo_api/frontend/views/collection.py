import logging
import traceback

from ..serializers import InstitutionSerializer, ResourceSerializer
from artigo.api.src.artigo_api.frontend.utils import media_url_to_image
from artigo.api.src.artigo_api.frontend.models import Institution, Resource
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class CollectionView(APIView):
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        collection = None

        collection_name = request.query_params.get('name')

        if collection_name:
            collection = get_collection_by_name(collection_name)

        if collection:
            return Response(collection)

        raise APIException('Unknown collection.')


def get_collection_by_name(collection_name):
    try:
        collection = Institution.objects.get(name__iexact=collection_name)
        resources = Resource.objects.filter(source_id=collection.id)
        resources = resources.exclude(hash_id__exact='')[:50]

        data = InstitutionSerializer(collection).data

        if resources.exists():
            data['resources'] = ResourceSerializer(resources, many=True).data

        return data
    except Exception as e:
        logger.error(traceback.format_exc())
