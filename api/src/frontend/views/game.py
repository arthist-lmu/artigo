import json
import logging
import traceback

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def add_tagging(request):
    try:
        body = request.body.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        body = request.body

    try:
        data = json.loads(body)
        # TODO: Eigentliche Abfrage hier -> add to Tagging table in DB

    except Exception as e:
        return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


# TODO: if tag in tagging already, then add to tag, if tag already in tag, don't add again
@require_http_methods(['POST'])
def add_tag(request):
    pass


# TODO: SELECT (-> QuerySet) first n tags that have been used most for this resource; if more than 5, randomly select?
@require_http_methods(['GET'])
def show_taboo_tags(request):
    pass


# TODO: SELECT (-> QuerySet)
@require_http_methods(['GET'])
def show_suggestions(request):
    pass


# TODO: SELECT (-> QuerySet)
@require_http_methods(['GET'])
def show_tags_to_combine(request):
    pass


