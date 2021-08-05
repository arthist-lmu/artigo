import json
import random
import logging
import traceback

from ..serializers import ResourceSerializer, TaggingSerializer
from frontend.utils import media_url_to_image
from frontend.models import Resource, Title, Tagging
from datetime import datetime
from django.db.models import Count
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def get_resource(request):
    try:
        body = request.body.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        body = request.body

    try:
        data = json.loads(body)
    except Exception as e:
        return JsonResponse({'status': 'error'})

    resource = None

    resource_id = data['params'].get('id')
    lang = data['params'].get('lang', 'en')

    if data['params'].get('random'):
        seed = datetime.now().strftime('%Y%m%d')
        resource = Resource.objects.random(seed)
        resource = get_resource_by_id(resource.id, lang)
    elif resource_id:
        resource = get_resource_by_id(resource_id, lang)

    if resource:
        return JsonResponse({'status': 'ok', 'data': resource})

    return JsonResponse({'status': 'error'})


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
            tags = taggings.values('tag').annotate(n=Count('tag'))
            tags = tags.order_by('-n').values('tag_id', 'tag__name', 'n')

            data['tags'] = TaggingSerializer(tags, many=True).data

        return data
    except Exception as e:
        logging.error(traceback.format_exc())
