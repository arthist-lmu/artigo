import random

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
from frontend.custom_renderers import *


class ARTigoGameView(APIView):
    """
    API View that retrieves the ARTigo game, allows users to post tags and so on
    """
    serializer_class = GametypeSerializer
    serializer_class = GamesessionSerializer
    serializer_class = GameroundSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class ARTigoTabooGameView(APIView):
    """
    API View that retrieves the ARTigo Taboo game, allows users to post tags and so on
    """
    serializer_class = GametypeSerializer
    serializer_class = GamesessionSerializer
    serializer_class = GameroundSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class TagATagGameView(APIView):
    """
    API View that retrieves the ARTigo game, allows users to post tags and so on
    """
    serializer_class = GametypeSerializer
    serializer_class = GamesessionSerializer
    serializer_class = GameroundSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class CombinoGameView(APIView):
    """
    API View that retrieves the ARTigo game, allows users to post tags and so on
    """
    serializer_class = GametypeSerializer
    serializer_class = GamesessionSerializer
    serializer_class = GameroundSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


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
        gametypes = Gametype.objects.all().order_by("name")
        return gametypes

    def get(self, request, *args, **kwargs):
        gametype = self.get_queryset()
        serializer = GametypeSerializer(gametype, many=True)
        return Response(serializer.data)


class GamesessionView(APIView):
    """
    API View that handles gamesessions
    """
    serializer_class = GamesessionSerializer

    def get_queryset(self):
        gamesessions = Gamesession.objects.all().filter(id=2015703320)
        return gamesessions

    def get(self, request, *args, **kwargs):
        gamesession = self.get_queryset()
        serializer = GamesessionSerializer(gamesession, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gamesession = request.data.get_queryset()
        serializer = GamesessionSerializer(data=gamesession)
        if serializer.is_valid(raise_exception=True):
            saved_gamesession = serializer.save()
        return Response(saved_gamesession)


class GametypeWithGamesessionView(APIView):
    """
    API View that handles gametypes with gamesessions
    """
    serializer_class = GametypeWithGamesessionSerializer

    def get_queryset(self):
        gametype = Gametype.objects.all().filter(name="imageLabeler")
        return gametype

    def get(self, request, *args, **kwargs):
        gametype = self.get_queryset()
        serializer = GametypeWithGamesessionSerializer(gametype, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gamesession = request.data.get_queryset()
        serializer = GametypeWithGamesessionSerializer(data=gamesession)
        if serializer.is_valid(raise_exception=True):
            saved_gamesession = serializer.save()
        return Response(saved_gamesession)


class GameroundView(APIView):
    """
    API endpoint that allows gamerounds to be viewed or edited
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
    API endpoint that allows taggings to be viewed or edited
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
        # tagging = request.data.get_queryset()
        Tagging.objects.create(id=request.data["id"],
                               tag=request.data["tag"],
                               gameround=request.data["gameround"],
                               resource=request.data["resource"]
                               )

        serializer = TaggingSerializer(data=request.data)
        if serializer.is_valid():
            # saved_tagging = serializer.save()
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(saved_tagging)


class TagView(APIView):
    """
    API endpoint that allows tags to be viewed or edited
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
        serializer = TagSerializer(data=request.data)
        Tag.objects.create(id=request.data["id"],
                           name=request.data["name"],
                           language=request.data["language"]
                           )

        if Tagging.objects.filter(tag=tag).exists():
            # tag_obj = Tag(name=request)
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

        if serializer.is_valid():
            # saved_tagging = serializer.save()
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(saved_tag)


class GameResourceView(APIView):
    """
    API view to handle resources
    """
    serializer_class = ResourceSerializer

    def get_queryset(self):
        resources = None
        while resources is None:
            random_idx = random.randint(0, Resource.objects.count() - 1)
            resources = Resource.objects.all().filter(id=random_idx)
        # TODO: See that a resource is always returned! check that resource not null
        return resources

    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = ResourceSerializer(resource, many=True)
        return Response(serializer.data)


class GameResourceViewPicture(APIView):
    """
    API view to handle resources
    """
    serializer_class = ResourceSerializer
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get_queryset(self):
        resources = None
        while resources is None:
            random_idx = random.randint(0, Resource.objects.count() - 1)
            resources = Resource.objects.all().filter(id=random_idx)
        return resources

    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = ResourceSerializer(resource, many=True)
        return Response(serializer.data)


class GameroundWithResourceView(APIView):
    """
    API view to handle gamerounds and resources/gameround
    """
    serializer_class = GameroundWithResourceSerializer

    def get_queryset(self):
        resources = None
        while resources is None:
            random_idx = random.randint(0, Resource.objects.count() - 1)
            resources = Resource.objects.all().filter(id=random_idx)
        # TODO: See that a resource is always returned! check that resource not null
        return resources

    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = GameroundWithResourceSerializer(resource, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gameround = request.data.get_queryset()
        serializer = GameroundSerializer(data=gameround)
        if serializer.is_valid(raise_exception=True):
            saved_gameround = serializer.save()
        return Response(saved_gameround)


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


