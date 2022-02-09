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


class GameViewController:
    """
    Class containing methods that control the order in which Game View methods get called
    also methods to check tags and calculate score & coordinate users
    """

    def get_random_object(self, MyModel):
        """Method that works for Tag a Tag game view"""
        random_object = None
        object_count = MyModel.objects.all().count() + 1
        while not MyModel.objects.all().filter(id=random_object).exists():
            for obj in range(object_count):
                n = random.randint(1, object_count)
                if MyModel.objects.all().filter(id=n).exists():
                    random_object = n
                    return random_object

    def get_random_id(self, MyModel):
        """Method for large querysets"""
        random_object = None
        object_count = MyModel.objects.all().count() + 1
        for obj in range(object_count):
            n = random.randint(1, object_count)
            while not MyModel.objects.all().filter(id=n).exists():
                alt = random.randint(1, object_count)
                if MyModel.objects.all().filter(id=alt).exists():
                    random_object = n

        return random_object

    def get_gameround_matching_resource(self, random_resource_id):
        """Checks if a previously played game round exists for a randomly chosen resource
        Returns a serialized gameround object (played previously for this same resource)
        """
        current_gameround = Gameround.objects.all().filter(taggings__resource_id=random_resource_id).order_by(
            "?").first()
        gameround_serializer = GameroundSerializer(current_gameround)

        return gameround_serializer.data

    def timer(self):
        """Start a new timer as soon as a gameround has been started/created"""
        start_time = datetime.now()
        elapsed_time = None
        if start_time is not None:
            elapsed_time = time.perf_counter()
        """Stop the timer, and return the elapsed time"""
        if start_time is None:
            elapsed_time = time.perf_counter() - start_time
        return elapsed_time

    def check_tagging_exists(self, tagging_to_check):
        """
        Matches tags entered with tags from the list of the tags from the matched Gameround object
        :return:
        """
        # tagging_to_check is Tagging object entered by user --> through POST request?!
        # matched_gameround = self.get_gameround_matching_resource() ?
        # TODO: REVIEW!!! after finishing post method
        if Tagging.objects.all().filter(tag=tagging_to_check).exists():

            new_tagging = Tagging.objects.create()
            tagging_serializer = TaggingSerializer(new_tagging)
            data = {'tagging': tagging_serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        elif not Tag.objects.all().filter(name=tagging_to_check).exists():
            new_tag = Tag.objects.create()
            tag_serializer = TagSerializer(new_tag)
            data = {'tagging': tag_serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def calculate_score(self):
        """Calculate per game round and per session score!? - maybe split method"""
        # returns JSON Object // HTTP Status code
        score_to_save = None
        data = None
        # 'Matching' here: match played round with a previously played round (25 p) and with entire DB->Tagging(5p)

        return Response(data, status=status.HTTP_201_CREATED)


class GametypeView(APIView):
    """
    API View that handles retrieving the correct type of a game
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
    retrieves an game session as well as a random resource per round
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """

    # TODO: USE LATER!!!!
    # renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        try:
            gametype = Gametype.objects.get(name="imageLabeler")
        except Gametype.DoesNotExist:
            print('There is no imageLabeler gametype in DB')
            return Response(status=status.HTTP_404_NOT_FOUND)
        # gametype = Gametype.objects.get(name="imageLabeler")
        gametype_serializer = GametypeSerializer(gametype)

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
        random_resource_2 = Resource.objects.all().order_by('?').first()
        second_resource_serializer = ResourceSerializer(random_resource_2)
        random_resource_3 = Resource.objects.all().order_by('?').first()
        third_resource_serializer = ResourceSerializer(random_resource_3)
        random_resource_4 = Resource.objects.all().order_by('?').first()
        fourth_resource_serializer = ResourceSerializer(random_resource_4)
        random_resource_5 = Resource.objects.all().order_by('?').first()
        fifth_resource_serializer = ResourceSerializer(random_resource_5)

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
            # return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        tag_serializer = TagSerializer(data=request.data)
        tagging_serializer = TaggingSerializer(data=request.data)
        gameround_id = request.data.get('gameround_id')
        gameround = Gameround.objects.get(id=gameround_id)

        # time where the gameround was created
        start_time = gameround.created
        # time 5 mins after gameround was created
        end_of_game = start_time + timedelta(seconds=60)
        if not datetime.utcnow().replace(tzinfo=pytz.UTC) >= end_of_game:
            if tagging_serializer.is_valid(raise_exception=True):
                tagging_serializer.save(tagging=request.data)
                return Response({"status": "success", "data": tagging_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": tag_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class ARTigoTabooGameView(APIView):
    """
    API View that retrieves the ARTigo Taboo game,
    5 Resource objects and gamerounds, along with a game session that is created on the spot
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def get(self, request, *args, **kwargs):
        gametype = Gametype.objects.get(name="imageLabeler_Taboo")
        gametype_serializer = GametypeSerializer(gametype)

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
        # time 5 mins after gameround was created
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
    """

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        controller = GameViewController()
        gametype = Gametype.objects.get(name="imageAndTagLabeler")
        gametype_serializer = GametypeSerializer(gametype)

        random_id = controller.get_random_object(Resource)
        resource_suggestions = Resource.objects.all().filter(id=random_id)
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
        # time 5 mins after gameround was created
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
    """

    def get(self, request, *args, **kwargs):
        gametype = Gametype.objects.get(name="Combino")
        gametype_serializer = GametypeSerializer(gametype)

        # resource_and_tags = Resource.objects.all().order_by('?').first()
        resource_and_tags = Resource.objects.all().get(id=327888)
        combination_serializer = CombinoTagsSerializer(resource_and_tags)

        # TODO: implement list of tags for tags from serializer - test in get to use in post!
        # tag = Tagging.objects.filter(resource__in=resource_and_tags).order_by('?').first()

        tags_list = []

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

        return Response({'resource and and tags to combine': combination_serializer.data,
                         # 'gameround': gameround_serializer.data
                         })

    def post(self, request, *args, **kwargs):

        combined_tagging_serializer = CombinationSerializer(data=request.data)

        if combined_tagging_serializer.is_valid(raise_exception=True):
            combined_tagging_serializer.save(combination=request.data)
            return Response({"status": "success", "data": combined_tagging_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": combined_tagging_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class GamesessionView(APIView):
    """
    API View that handles gamesessions
    """

    def get(self, request, *args, **kwargs):
        gamesession = Gamesession.objects.all().order_by('?').first()
        serializer = GamesessionSerializer(gamesession)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gamesession_serializer = GamesessionSerializer(data=request.data)
        if gamesession_serializer.is_valid(raise_exception=True):
            gamesession_serializer.save(gamesession=request.data)
            return Response({"status": "success", "data": gamesession_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": gamesession_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class GameroundView(APIView):
    """
    API endpoint that allows gamerounds to be viewed or edited
    """

    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        gameround_serializer = GameroundSerializer(data=request.data)
        if gameround_serializer.is_valid(raise_exception=True):
            gameround_serializer.save(gameround=request.data)
            return Response({"status": "success", "data": gameround_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": gameround_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class TaggingView(APIView):
    """
    API endpoint that allows taggings to be viewed or edited
    """

    def get(self, request, *args, **kwargs):
        """Retrieves a random Tag"""
        # request.session.set_expiry(30)
        tagging = Tagging.objects.all().order_by('?').first()
        tagging_serializer = TagATagTaggingSerializer(tagging)
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
    API endpoint for combino
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
            return Response({"status": "success", "data": combined_tagging_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": combined_tagging_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    """
    API endpoint that allows tags to be viewed or edited
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
    """

    def get(self, request, *args, **kwargs):
        resource = Resource.objects.all().order_by('?').first()
        serializer = ResourceSerializer(resource)
        return Response({
            'resource': serializer.data
        })


class GameResourceViewPicture(APIView):
    """
    API view to handle resources
    """
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        resource = Resource.objects.all().order_by('?').first()
        serializer = ResourceSerializer(resource)
        return Response({
            'resource and tags to combine': serializer.data
        })
