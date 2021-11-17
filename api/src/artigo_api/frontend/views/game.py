import json
import logging
import traceback

from frontend.models import Tagging, Tag
from frontend.serializers import *

from rest_framework.parsers import JSONParser
from rest_framework import status

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
        if request.method == 'POST':
            tagging_data = JSONParser.parse(request)
            tagging_serializer = TaggingSerializer(data=tagging_data)

            if tagging_serializer.is_valid():
                tagging_serializer.save()
                return JsonResponse(tagging_serializer.data, status=status.HTTP_201_CREATED)

            return JsonResponse(tagging_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


# TODO: if tag in tagging already, then add to tag, if tag already in tag, don't add again
@require_http_methods(['POST'])
def add_tag(request):
    tag_data = JSONParser.parse(request)
    tag_serializer = TaggingSerializer(data=tag_data)

    if tag_serializer.is_valid():
        tag_serializer.save()
        return JsonResponse(tag_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: SELECT (-> QuerySet) first n tags that have been used most for this resource; if more than 5, randomly select?
@require_http_methods(['GET'])
def show_taboo_tags(request):
    taboo_tags = Tag.objects.filter()
    taboo_tag_serializer = TagSerializer(data=taboo_tags)

    if request.method == 'GET':
        taboo_tag_serializer = TagSerializer(taboo_tags, many=True)
        return JsonResponse(taboo_tag_serializer.data, safe=False)
    return JsonResponse(taboo_tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: SELECT (-> QuerySet)
@require_http_methods(['GET'])
def show_suggestions(request):
    suggested_tags = Tag.objects.filter()
    suggested_tag_serializer = TagSerializer(data=suggested_tags)

    if request.method == 'GET':
        suggested_tag_serializer = TagSerializer(suggested_tags, many=True)
        return JsonResponse(suggested_tag_serializer.data, safe=False)
    return JsonResponse(suggested_tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: SELECT (-> QuerySet)
@require_http_methods(['GET'])
def show_tags_to_combine(request):
    tags_to_combine = Tag.objects.filter()
    tags_to_combine_serializer = TagSerializer(data=tags_to_combine)

    if request.method == 'GET':
        suggested_tag_serializer = TagSerializer(tags_to_combine, many=True)
        return JsonResponse(tags_to_combine_serializer.data, safe=False)
    return JsonResponse(tags_to_combine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
