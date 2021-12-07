from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser

from frontend.models import *
from frontend.serializers import *


class ARTigoGametypeView(APIView):
    """
    API View that handles retrieving the ARTigo game view
    """
    serializer_class = GametypeSerializer

    def get_queryset(self):
        gametypes = Gametype.objects.all().filter(name="imageLabeler")
        return gametypes

    def get(self, request, *args, **kwargs):
        gametype = self.get_queryset()
        serializer = GametypeSerializer(gametype, many=True)
        return Response(serializer.data)


class GametypeView(APIView):
    """
    API View that handles retrieving the correct type of a game
    """
    serializer_class = GametypeSerializer

    def get_queryset(self):
        gametypes = Gametype.objects.all()
        return gametypes

    def get(self, request, *args, **kwargs):
        gametype = self.get_queryset()
        serializer = GametypeSerializer(gametype, many=True)
        return Response(serializer.data)


class GamesessionView(APIView):
    """
    API View that handles gamesessions
    """
    serializer_class = GamesessionSerializer2

    def get_queryset(self):
        gamesessions = Gamesession.objects.all().filter(created="March 27, 2017, 7:57 p.m.")
        return gamesessions

    def get(self, request, *args, **kwargs):
        gamesession = self.get_queryset()
        serializer = GamesessionSerializer2(gamesession, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gamesession = request.data.get_queryset()

        serializer = GamesessionSerializer2(data=gamesession)
        if serializer.is_valid(raise_exception=True):
            saved_gamesession = serializer.save()
        return Response(saved_gamesession)


class GameroundView(APIView):
    """
    API View that handles gamerounds
    """
    serializer_class = GameroundSerializer

    def get_queryset(self):
        gamerounds = Gameround.objects.all()
        return gamerounds

    def get(self, request, *args, **kwargs):
        gameround = self.get_queryset()
        serializer = GameroundSerializer(gameround, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gameround = request.data.get_queryset()

        serializer = GameroundSerializer(data=gameround)
        if serializer.is_valid(raise_exception=True):
            saved_gameround = serializer.save()
        return Response(saved_gameround)


class TaggingView(APIView):
    """
    API View to do everything to do with taggings
    """
    serializer_class = TaggingSerializer

    def get_queryset(self):
        taggings = Tagging.objects.all().filter(resource=8225)
        return taggings

    def get(self, request, *args, **kwargs):
        tagging = self.get_queryset()
        serializer = TaggingSerializer(tagging, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        tagging = request.data.get_queryset()

        serializer = TaggingSerializer(data=tagging)
        if serializer.is_valid(raise_exception=True):
            saved_tagging = serializer.save()
        return Response(saved_tagging)


class TagView(APIView):
    """
    API View that deals with tags
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        tags = Tag.objects.all().filter(language="fr")
        # serializer = TagSerializer(tags, many=True)
        return tags

    def get(self, request, *args, **kwargs):
        tag = self.get_queryset()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        tag = request.data.get_queryset()

        if Tagging.objects.filter(tag=tag).exists():
            new_tag = Tag()
            new_tag.name = tag
            new_tag.save()
            serializer = TagSerializer(data=tag)
            if serializer.is_valid(raise_exception=True):
                saved_tag = serializer.save()
        else:
            new_tag = Tagging()
            new_tag.tag = user_tag
            new_tag.save()

        return Response(saved_tag)


class GameResourceView(APIView):
    """
    API view to
    """
    serializer_class = ResourceSerializer

    def get_queryset(self):
        resources = Resource.objects.all().filter(hash_id="6822d12bdd1b30b686528bea8abffcaf")
        return resources

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = ResourceSerializer(resource, many=True)
        return Response(serializer.data)


class TabooTagsView(APIView):
    """
    API View that handles display of Taboo Tags during ARTigo Taboo
    """
    serializer_class = TabooTagSerializer

    def get_queryset(self):
        tags = Tagging.objects.all().filter(language="fr", tag="café")
        return tags

    def get(self, request, *args, **kwargs):
        tag = self.get_queryset()
        serializer = TabooTagSerializer(tag, many=True)
        return Response(serializer.data)


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


def save_to_tag():
    pass


def get_custom_tags():
    pass


def check_tag_exists():
    """
    Checks if another tagging string for the same resource has been added before, which is the same as the entered string
    :return:
    """
    tagging_to_check.get_queryset(tagging)
    serializer = TaggingSerializer(tagging_to_check)
    if Tagging.objects.filter(tag=tagging_to_check).exists():
        pass


def calculate_score():
    pass


