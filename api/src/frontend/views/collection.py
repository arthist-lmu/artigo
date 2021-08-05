import json
import logging
import traceback

from ..serializers import SourceSerializer, ResourceSerializer
from frontend.utils import media_url_to_image
from frontend.models import Source, Resource
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def get_collection(request):
    try:
        body = request.body.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        body = request.body

    try:
        data = json.loads(body)
    except Exception as e:
        return JsonResponse({'status': 'error'})

    collection = None

    collection_name = data['params'].get('name')

    if collection_name:
        collection = get_collection_by_name(collection_name)

    if collection:
        return JsonResponse({'status': 'ok', 'data': collection})

    return JsonResponse({'status': 'error'})


def get_collection_by_name(collection_name):
    try:
        collection = Source.objects.get(name__iexact=collection_name)
        resources = Resource.objects.filter(source_id=collection.id)
        resources = resources.exclude(hash_id__exact='')[:50]

        data = SourceSerializer(collection).data

        if resources.exists():
            data['resources'] = ResourceSerializer(resources, many=True).data

        return data
    except Exception as e:
        logging.error(traceback.format_exc())
