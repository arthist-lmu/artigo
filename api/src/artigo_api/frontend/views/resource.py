import random
import logging
import traceback

from frontend.utils import media_url_to_image
from frontend.models import Resource, Title, Tagging
from frontend.serializers import ResourceSerializer, TagCountSerializer
from datetime import datetime
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)


class ResourceView(APIView):
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        resource = None

        resource_id = request.query_params.get('id')
        lang = request.query_params.get('lang', 'en')

        if request.query_params.get('random'):
            seed = datetime.now().strftime('%Y%m%d')
            resource_id = Resource.objects.random(seed).id

        if resource_id:
            resource = get_resource_by_id(resource_id, lang)

        if resource:
            return Response(resource)

        raise NotFound(detail='Unknown resource', code=404)


def get_resource_by_id(resource_id, lang=None):
    try:
        resource = Resource.objects.get(id=resource_id)
        taggings = Tagging.objects.filter(resource_id=resource.id)

        if lang:
            taggings = taggings.filter(tag__language=lang)

        data = ResourceSerializer(resource).data

        if data.get('hash_id'):
            data['path'] = media_url_to_image(data['hash_id'])

        if taggings.exists():
            tags = taggings.values('tag').annotate(count=Count('tag'))
            tags = tags.values('tag_id', 'tag__name', 'tag__language', 'count')

            data['tags'] = TagCountSerializer(tags, many=True).data

        return data
    except Exception as e:
        logger.error(traceback.format_exc())

        # post here to res return based on game param
