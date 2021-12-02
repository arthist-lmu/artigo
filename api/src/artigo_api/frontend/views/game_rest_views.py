from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser

from frontend.models import *
from frontend.serializers import *


# TODO: Alternatively try one APIView per game (1 game: 1 class)? would that work?

class GametypeView(APIView):
    """
    API View that handles retrieving the correct type of a game
    """
    serializer_class = GametypeSerializer

    # @api_view(['GET'])
    def get_queryset(self):
        gametypes = Gametype.objects.all()
        serializer = GametypeSerializer(gametypes, many=True)
        return Response(serializer.data)

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        gametype = self.get_queryset()
        serializer = GametypeSerializer(gametype)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     gametype = self.get_queryset(pk)
    #     serializer = GametypeSerializer(gametype, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     gametype = self.get_queryset(pk)
    #     gametype.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class TaggingView(APIView):
    """
    API View to do everything to do with taggings
    """
    serializer_class = TaggingSerializer

    # @method_decorator(cache_page(60 * 60 * 2))
    def get_queryset(self):
        taggings = Tagging.objects.all()
        serializer = TaggingSerializer(taggings, many=True)
        return Response(serializer.data)

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        tagging = self.get_queryset()
        serializer = TaggingSerializer(tagging)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     tagging = self.get_queryset(pk)
    #     serializer = TaggingSerializer(tagging, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     tagging = self.get_queryset(pk)
    #     tagging.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


def check_tag_exists(self, request, tagging, format=None):
    """
    Checks if another tagging string for the same resource has been added before, which is the same as the entered string
    :return:
    """
    tagging_to_check = self.get_queryset(tagging)
    serializer = TaggingSerializer(tagging_to_check)
    if Tagging.objects.filter(tag=tagging_to_check).exists():
        pass


def calculate_score():
    pass


class TagView(APIView):
    """
    API View that deals with tags
    """
    serializer_class = TagSerializer

    def get_tag(self, request, format=None):
        tags = Tag.objects.all()
        return tags

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        tag = self.get_tag()
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tag = self.get_tag(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tag = self.get_tag(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def save_to_tag():
    pass


def get_custom_tags():
    pass


class GameResourceView(APIView):
    """
    API view to
    """
    serializer_class = ResourceSerializer

    def get_resource(self):
        """
        Returns all tags
        :param request:
        :param format:
        :return:
        This is the queryset!
        """
        resources = Resource.objects.all()
        return resources

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        resource = self.get_resource(request)
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ARTigoGameView(APIView):

    def save_tags(self, user_tag):
        if Tagging.objects.filter(tag=user_tag).exists():
            new_tag = Tag()
            new_tag.name = user_tag
            new_tag.save()
        else:
            new_tag = Tagging()
            new_tag.tag = user_tag
            new_tag.save()




