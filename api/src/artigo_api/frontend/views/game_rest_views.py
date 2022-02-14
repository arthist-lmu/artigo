import random

import time
from datetime import datetime, timedelta

import pytz
from django.utils import timezone

from rest_framework import status, renderers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import (
    HTMLFormRenderer,
    JSONRenderer,
    BrowsableAPIRenderer,
)
from frontend.models import *
from frontend.serializers import *
from frontend.custom_renderers import *


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class GametypeView(APIView):
    """
    API View that handles retrieving game types
    """

    def get_queryset(self):
        gametypes = Gametype.objects.all()
        return gametypes

    def get(self, request, *args, **kwargs):
        """ Iterates through all gametype objects and chooses the correct one"""
        name = request.GET.get("name")

        serializer = None
        gametype = self.get_queryset()

        if gametype is None:
            while serializer is None:
                if name == "imageLabeler":
                    while gametype is None:
                        gametype = self.get_queryset().filter(name="imageLabeler")
                if name == "imageLabeler_Taboo":
                    while gametype is None:
                        gametype = self.get_queryset().filter(name="imageLabeler_Taboo")
                if name == "imageAndTagLabeler":
                    while gametype is None:
                        gametype = self.get_queryset().filter(name="imageAndTagLabeler")
                if name == "Combino":
                    while gametype is None:
                        gametype = self.get_queryset().filter(name="Combino")
        serializer = GametypeSerializer(gametype, many=True)
        return Response({'gametype': serializer.data})


class ARTigoGameView(APIView):
    """
    API View that retrieves the ARTigo game,
    get:
    retrieves an game session as well as a random resource per game round

    post:
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """
    # can be used later
    # renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        try:
            gametype = Gametype.objects.get(name="imageLabeler")
        except Gametype.DoesNotExist:
            print('There is no imageLabeler gametype in DB')
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(user_id=current_user_id,
                                                 gametype=gametype,
                                                 created=datetime.now())

        random_resource_1 = Resource.objects.all().order_by('?').first()
        first_resource_serializer = ResourceSerializer(random_resource_1)
        # random_resource_2 = Resource.objects.all().order_by('?').first()
        # second_resource_serializer = ResourceSerializer(random_resource_2)
        # random_resource_3 = Resource.objects.all().order_by('?').first()
        # third_resource_serializer = ResourceSerializer(random_resource_3)
        # random_resource_4 = Resource.objects.all().order_by('?').first()
        # fourth_resource_serializer = ResourceSerializer(random_resource_4)
        # random_resource_5 = Resource.objects.all().order_by('?').first()
        # fifth_resource_serializer = ResourceSerializer(random_resource_5)

        gameround = Gameround.objects.create(user_id=current_user_id,
                                             gamesession=gamesession,
                                             created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                             score=current_score)

        gameround_serializer = GameroundSerializer(gameround)

        start_time = gamesession.created
        end_of_game = start_time + timedelta(minutes=5)

        if not datetime.now() >= end_of_game:
            return Response({'resource': first_resource_serializer.data, 'gameround': gameround_serializer.data,})
        else:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    def post(self, request, *args, **kwargs):
        tag_serializer = TagSerializer(data=request.data)
        tagging_serializer = TaggingSerializer(data=request.data)
        gameround_id = request.data.get('gameround_id')
        gameround = Gameround.objects.get(id=gameround_id)

        # time where the gameround was created
        start_time = gameround.created
        # time 1 mins after gameround was created
        end_of_game = start_time + timedelta(seconds=60)
        if not datetime.utcnow().replace(tzinfo=pytz.UTC) >= end_of_game:
            if tagging_serializer.is_valid(raise_exception=True):
                tagging_serializer.save(tagging=request.data)
                return Response({"status": "success", "data": tagging_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": tag_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class ARTigoTabooGameView(APIView):
    """
    API View that retrieves the ARTigo Taboo game,
    get:
    retrieves an game session and a random resource per game round

    post:
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """

    def get(self, request, *args, **kwargs):
        try:
            gametype = Gametype.objects.get(name="imageLabeler_Taboo")
        except Gametype.DoesNotExist:
            print('There is no imageLabeler_Taboo gametype in DB')
            return Response(status=status.HTTP_404_NOT_FOUND)

        resource_suggestions = Resource.objects.all().order_by('?').first()
        resource_serializer = TabooTagSerializer(resource_suggestions)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )
        gameround_serializer = GameroundSerializer(gameround)

        start_time = gamesession.created
        end_of_game = start_time + timedelta(minutes=5)

        if not datetime.now() >= end_of_game:
            return Response({'resource and taboo input': resource_serializer.data,
                             'gameround': gameround_serializer.data})

    def post(self, request, *args, **kwargs):
        tag_serializer = TagSerializer(data=request.data)
        tagging_serializer = TabooTaggingSerializer(data=request.data)
        gameround_id = request.data.get('gameround_id')
        gameround = Gameround.objects.get(id=gameround_id)

        # time where the gameround was created
        start_time = gameround.created
        # time 1 mins after gameround was created
        end_of_game = start_time + timedelta(seconds=60)

        if not datetime.utcnow().replace(tzinfo=pytz.UTC) >= end_of_game:
            if tagging_serializer.is_valid(raise_exception=True):
                tagging_serializer.save(tagging=request.data)
                return Response({"status": "success", "data": tagging_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": tag_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class TagATagGameView(APIView):
    """
    API endpoint that retrieves the Tag a Tag game
    get:
    retrieves a game session and a random resource as well as a tag and a list of suggested tags per game round

    post:
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """

    def get(self, request, *args, **kwargs):
        try:
            gametype = Gametype.objects.get(name="imageAndTagLabeler")
        except Gametype.DoesNotExist:
            print('There is no imageAndTagLabeler gametype in DB')
            return Response(status=status.HTTP_404_NOT_FOUND)

        random_id = Resource.objects.all().order_by('?').first()
        resource_suggestions = Resource.objects.all().filter(id=random_id.id)
        suggestions_serializer = SuggestionsSerializer(resource_suggestions, many=True)

        tag = Tagging.objects.filter(resource__in=resource_suggestions).order_by('?').first()
        tagging_serializer = TaggingSerializer(tag)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )
        gameround_serializer = GameroundSerializer(gameround)
        start_time = gamesession.created
        end_of_game = start_time + timedelta(minutes=5)

        if not datetime.now() >= end_of_game:
            return Response({'tag': tagging_serializer.data,
                             'resourceand and suggestions': suggestions_serializer.data,
                             'gameround': gameround_serializer.data})

    def post(self, request, *args, **kwargs):
        tag_serializer = TagSerializer(data=request.data)
        tagging_serializer = TagATagTaggingSerializer(data=request.data)
        gameround_id = request.data.get('gameround_id')
        gameround = Gameround.objects.get(id=gameround_id)

        # time where the gameround was created
        start_time = gameround.created
        # time 1 mins after gameround was created
        end_of_game = start_time + timedelta(seconds=60)

        if not datetime.utcnow().replace(tzinfo=pytz.UTC) >= end_of_game:
            if tagging_serializer.is_valid(raise_exception=True):
                tagging_serializer.save(tagging=request.data)
                return Response({"status": "success", "data": tagging_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": tag_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class CombinoGameView(APIView):
    """
    API endpoint that retrieves the Combino game view
    get:
    retrieves an game session and a random resource per game round as well as a list of tags to combine during a round

    post:
    allows users to post combinations of 2 tags that are verified and saved accordingly to the Combination table
    """

    def get(self, request, *args, **kwargs):
        try:
            gametype = Gametype.objects.get(name="Combino")
        except Gametype.DoesNotExist:
            print('There is no Combino gametype in DB')
            return Response(status=status.HTTP_404_NOT_FOUND)

        resource_and_tags = Resource.objects.all().order_by('?').first()
        combination_serializer = CombinoTagsSerializer(resource_and_tags)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )

        gameround_serializer = GameroundSerializer(gameround)

        start_time = gamesession.created
        end_of_game = start_time + timedelta(minutes=5)

        if not datetime.now() >= end_of_game:

            return Response({'resource and and tags to combine': combination_serializer.data,
                             'gameround': gameround_serializer.data
                             })

    def post(self, request, *args, **kwargs):

        combined_tagging_serializer = CombinationSerializer(data=request.data)
        gameround_id = request.data.get('gameround_id')
        gameround = Gameround.objects.get(id=gameround_id)

        # time where the gameround was created
        start_time = gameround.created
        # time 1 mins after gameround was created
        end_of_game = start_time + timedelta(seconds=60)

        if not datetime.utcnow().replace(tzinfo=pytz.UTC) >= end_of_game:

            if combined_tagging_serializer.is_valid(raise_exception=True):
                combined_tagging_serializer.save(combination=request.data)
                return Response({"status": "success", "data": combined_tagging_serializer.data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": combined_tagging_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class GamesessionView(APIView):
    """
    API View that handles gamesessions
    get:
    retrieves an random game session
    """

    def get(self, request, *args, **kwargs):
        gamesession = Gamesession.objects.all().order_by('?').first()
        serializer = GamesessionSerializer(gamesession)
        return Response(serializer.data)


class GameroundView(APIView):
    """
    API endpoint that allows gamerounds to be viewed or edited
    get:
    retrieves a random game round
    """

    def get(self, request, *args, **kwargs):
        # Outcommented code used for testing
        # random_resource = Resource.objects.all().order_by('?').first()
        # resource_serializer = ResourceSerializer(random_resource)  # Response is a serialized JSON object
        # random_resource_id = random_resource.id  # id of the random Resource for the game round
        # gameround = Gameround.objects.all().filter(taggings__resource_id=random_resource_id).order_by("?").first()
        gameround = Gameround.objects.all().order_by("?").first()
        gameround_serializer = GameroundSerializer(gameround)

        return Response({
            # 'resource to coordinate': resource_serializer.data,
            'gameround': gameround_serializer.data,
        })


class TaggingView(APIView):
    """
    API endpoint that allows taggings to be viewed or edited
    get:
    retrieves a random tagging

    post:
    allows users to post taggings that are verified and saved accordingly to the Tagging table
    """

    def get(self, request, *args, **kwargs):
        """Retrieves a random Tag"""
        tagging = Tagging.objects.all().order_by('?').first()
        tagging_serializer = TaggingSerializer(tagging)
        return Response({'tagging only': tagging_serializer.data})

    def post(self, request, *args, **kwargs):
        tagging_serializer = TaggingSerializer(data=request.data)
        if tagging_serializer.is_valid(raise_exception=True):
            tagging_serializer.save(tagging=request.data)
            return Response({"status": "success", "data": tagging_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": tagging_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CombinationView(APIView):
    """
    API endpoint for combinations
    get:
    retrieves a random combination

    post:
    allows users to enter a combination
    """

    def get(self, request, *args, **kwargs):
        """Retrieves a random Tag"""
        tagging = Combination.objects.all().order_by('?').first()
        tagging_serializer = CombinationSerializer(tagging)
        return Response({'combination': tagging_serializer.data})

    def post(self, request, *args, **kwargs):
        combined_tagging_serializer = CombinationSerializer(data=request.data)

        if combined_tagging_serializer.is_valid(raise_exception=True):
            combined_tagging_serializer.save(combination=request.data)
            return Response({"status": "success", "data": combined_tagging_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": combined_tagging_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    """
    API endpoint that allows tags to be viewed or edited
    get:
    retrieves a random tag from the database

    post:
    allows users to post tags that are verified and saved accordingly to the Tag table
    """

    def get(self, request, *args, **kwargs):
        tag = Tag.objects.all().order_by('?').first()
        tag_serializer = TagWithIdSerializer(tag)
        return Response(tag_serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(tag=request.data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GameResourceView(APIView):
    """
    API view to handle resources
    get:
    retrieves a random resource object
    """

    def get(self, request, *args, **kwargs):
        resource = Resource.objects.all().order_by('?').first()
        serializer = ResourceSerializer(resource)
        return Response({
            'resource': serializer.data
        })

