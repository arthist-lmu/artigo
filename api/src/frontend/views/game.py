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
    except Exception as e:
        return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
