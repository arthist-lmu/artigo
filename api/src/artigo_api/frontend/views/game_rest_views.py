import random

import time
from datetime import datetime

from rest_framework import status, renderers
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


class GameViewController:
    """
    Class containing methods that control the order in which Game View methods get called
    also methods to check tags and calculate score & coordinate users
    """

    def get_gameround(self):
        current_gameround = None
        return current_gameround

    def get_gamesession(self):
        current_gamesession = None
        return current_gamesession

    def get_time_created(self):
        pass

    def get_resource(self):
        current_resource = Resource.objects.all() # should return the current resource of the round
        return current_resource

    def check_tag_exists(self, tagging_to_check):
        """
        Checks if another tagging string for the same resource has been added before, which is the same as the entered string
        :return:
        """
        saved_tagging = None
        saved_tag = None

        tagging_serializer = TaggingSerializer(tagging_to_check)
        tag_serializer = TagSerializer(tagging_to_check)
        random_id = None

        tagging_to_check.get_queryset()

        while saved_tagging is None or saved_tag is None:
            # TODO: check if condition is ok
            if Tagging.objects.filter(tag=tagging_to_check).exists():
                saved_tag = Tag()

                while random_id is None:
                    random_number = random.randint(0, Tag.objects.count() - 1)
                    if Tag.objects.filter(id=random_number).exists():
                        random_number_alternative = random.randint(0, Tag.objects.count() - 1)
                        random_id = random_number_alternative
                    else:
                        random_id = random_number

                saved_tag.id = random_id
                saved_tag.name = tagging_to_check
                saved_tag.language = tagging_to_check.language
                saved_tag = tag_serializer.save()
                return Response(saved_tag, status=status.HTTP_201_CREATED)
            else:
                saved_tagging = Tagging()
                while random_id is None:
                    random_number = random.randint(0, Tagging.objects.count() - 1)
                    if Tagging.objects.filter(id=random_number).exists():
                        random_number_alternative = random.randint(0, Tagging.objects.count() - 1)
                        random_id = random_number_alternative
                    else:
                        random_id = random_number
                saved_tagging.id = random_id
                saved_tagging.tag = tagging_to_check
                saved_tagging.gameround = self.get_gameround()
                saved_tagging.score = self.calculate_score(tagging_to_check, saved_tagging.gameround)
                saved_tagging.created = self.get_time_created()
                saved_tagging.resource = self.get_resource()
                saved_tagging = tagging_serializer.save()
                return Response(saved_tagging, status=status.HTTP_200_OK)

    def tag_exists(self):
        if self.check_tag_exists(tagging) == status.HTTP_200_OK:
            return True
        else:
            return False

    def calculate_score(self, tagging_to_check, gameround):
        # returns JSON Object // HTTP Status code
        score_to_save = None
        saved_tagging = None
        # 'Matching' here: match played round with a previously played round (25 p) and with entire DB->Tagging(5p)

        return Response(saved_tagging, status=status.HTTP_201_CREATED)

    def timer(self, start):
        """Start a new timer"""
        start_time = start
        elapsed_time = None
        if start_time is not None:
            start_time = time.perf_counter()
        """Stop the timer, and return the elapsed time"""
        if start_time is None:
            elapsed_time = time.perf_counter() - start_time
        return elapsed_time

    # TODO: finish this before post!
    def coordinate_players(self, current_gameround):
        """Check DB for previously played gameround"""
        gamerounds = Gameround.objects.all()
        gamesessions = Gamesession.objects.all()

        if gamerounds.filter().exists():
            pass

    def start_game(self, gametype, gameround):

        self.coordinate_players(gameround)

    def generate_random_id(self, MyModel):
        """ Picks a random id for an object"""
        random_object = None
        if random_object is None:
            random_object = random.randrange(1, MyModel.objects.all().count() + 1)
            while MyModel.objects.all().filter(id=random_object).exists():
                random_object = random.randrange(1, MyModel.objects.all().count() + 1)
            return random_object

    def pick_random_object(self, MyModel):
        """ Picks a random id for an object, checks if object with that id exists and returns the random number"""
        random_object = None
        if random_object is None:
            random_object = random.randrange(1, MyModel.objects.all().count() + 1)
            while not MyModel.objects.all().filter(id=random_object).exists():
                random_object = random.randrange(1, MyModel.objects.all().count() + 1)
            return random_object


class GametypeView(APIView):
    """
    API View that handles retrieving the correct type of a game
    """
    serializer_class = GametypeSerializer

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
    retrieves an empty game session to be filled with the necessary data and sent back to the server
    retrieves a random resource per round
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """

    # TODO: USE LATER!!!!
    # renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        gametype = Gametype.objects.all().filter(name="imageLabeler")
        gametype_serializer = GametypeSerializer(gametype, many=True)

        # TODO: Build timer in!!!
        # controller.timer()
        # rounds = gametype.rounds

        # for round in rounds:
        # for every round in the game session, load a randomly chosen resource and an empty gameround
        gameround = Gameround.objects.none()
        gameround_serializer = GameroundSerializer(gameround, many=True)

        # duration = gametype.round_duration
        # round = gameround

        # while duration is not None:
        random_resource = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        resource_serializer = ResourceSerializer(random_resource, many=True)

        gamesession = Gamesession.objects.none()
        gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        # TODO: only save if 5 rounds have been played! Tags/Taggings can be saved - find a way!
        return Response({'gametype': gametype_serializer.data,
                         'resource': resource_serializer.data,
                         'gameround': gameround_serializer.data,
                         'gamesession': gamesession_serializer.data
                         })


def post(self, request, *args, **kwargs):
    controller = GameViewController()
    saved_tagging = None
    saved_tag = None
    current_user = CustomUserSerializer(data=request.user)  # user instance
    serializer = TaggingSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # saved_tagging = Tagging.objects.create(id=controller.generate_random_id(Tagging),
        #                                        user=current_user,
        #                                        gameround=current_user.data["gameround"],
        #                                        resource=request.data["resource"],
        #                                        tag=request.data["tag"],
        #                                        created=request.data["created"],
        #                                        score=request.data["score"],
        #                                        origin=request.data["origin"]
        #                                        )
        # saved_tagging.save()
        serializer = TaggingSerializer(saved_tagging)
        return Response({'status': 'success', 'tagging': serializer.data}, status=status.HTTP_200_OK)

    if saved_tagging is None:
        return Response({'tagging': serializer.data}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(saved_tagging, status=status.HTTP_400_BAD_REQUEST)
    # TODO: Resource id has to be sent with tag/tagging! ?

    # if saved_tagging.exists():
    # saved_tag =


class ARTigoTabooGameView(APIView):
    """
    API View that retrieves the ARTigo Taboo game,
    retrieves an empty game session to be filled with the necessary data and sent back to the server
    retrieves a random resource per round along with the taboo tags for the respective resource
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        gametype = Gametype.objects.all().filter(name="imageLabeler_Taboo")
        gametype_serializer = GametypeSerializer(gametype, many=True)

        resource_suggestions = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        resource_serializer = TabooTagSerializer(resource_suggestions, many=True)

        # TODO: ask again if empty object neccessary
        gameround = Gameround.objects.none()
        gameround_serializer = GameroundSerializer(gameround, many=True)

        gamesession = Gamesession.objects.none()
        gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({'gametype': gametype_serializer.data,
                         'resource and taboo input': resource_serializer.data,
                         'gameround': gameround_serializer.data,
                         'gamesession': gamesession_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        controller = GameViewController()
        saved_tag = None
        current_user = CustomUserSerializer(data=request.user)  # user instance
        tag_serializer = TagSerializer(data=request.data)

        if tag_serializer.is_valid(raise_exception=True):
            saved_tag = Tag.objects.create(id=controller.generate_random_id(Tag),
                                           tag=request.data["name"],
                                           language=request.data["language"]
                                           )
            saved_tag.save()
            tag_serializer = TagSerializer(saved_tag)
            return Response({'status': 'success', 'tag': tag_serializer.data}, status=status.HTTP_200_OK)

        if saved_tag is None:
            return Response({'tagging': tag_serializer.data}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(saved_tag, status=status.HTTP_400_BAD_REQUEST)


class TagATagGameView(APIView):
    """
    API endpoint that retrieves the Tag a Tag game
    """

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        controller = GameViewController()
        gametype = Gametype.objects.all().filter(name="imageAndTagLabeler")
        gametype_serializer = GametypeSerializer(gametype, many=True)

        resource_suggestions = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        suggestions_serializer = SuggestionsSerializer(resource_suggestions, many=True)

        # TODO: Try implementing special serializer to get the most used tag per resource
        # tag = Tagging.objects.none()
        # tag = Tagging.objects.all().filter(id=controller.pick_random_object(Tagging))
        # tagging_serializer = TaggingSerializer(tag, many=True)
        tag = Tagging.objects.all().get(resource=resource_suggestions)
        tagging_serializer = HighestTagCountSerializer(tag)

        # TODO: ask again if empty object neccessary
        gameround = Gameround.objects.none()
        gameround_serializer = GameroundSerializer(gameround, many=True)

        gamesession = Gamesession.objects.none()
        gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({
            'gametype': gametype_serializer.data,
            'tag': tagging_serializer.data,
            'resource and suggestions': suggestions_serializer.data,
            'gameround': gameround_serializer.data,
            'gamesession': gamesession_serializer.data
        })


def post(self, request, *args, **kwargs):
    saved_tagging = None

    serializer = TaggingSerializer(data=request.data)

    if serializer.is_valid() and saved_tagging is not None:

        serializer.save()
        return Response({'tagging': serializer.data}, status=status.HTTP_201_CREATED)

    elif saved_tagging is None:
        return Response({'tagging': serializer.data}, status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'tagging': serializer.data}, status=status.HTTP_400_BAD_REQUEST)


class CombinoGameView(APIView):
    """
    API endpoint that retrieves the Combino game view
    """

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""

        controller = GameViewController()
        gametype = Gametype.objects.all().filter(name="Combino")
        gametype_serializer = GametypeSerializer(gametype, many=True)

        resource_and_tags = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        combination_serializer = CombinoTagsSerializer(resource_and_tags, many=True)

        # TODO: ask again if empty object neccessary
        gameround = Gameround.objects.none()
        gameround_serializer = GameroundSerializer(gameround, many=True)

        gamesession = Gamesession.objects.none()
        gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({
            'gametype': gametype_serializer.data,
            'resource and tags to combine': combination_serializer.data,
            'gameround': gameround_serializer.data,
            'gamesession': gamesession_serializer.data
        })

    def post(self, request, *args, **kwargs):
        saved_combined_tagging = None
        # TODO: add correct serializer here
        combined_tagging = ResourceWithTaggingsSerializer(data=request.data)
        while saved_combined_tagging is None:
            serializer = ResourceWithTaggingsSerializer(data=combined_tagging)
            if serializer.is_valid(raise_exception=True):
                saved_combined_tagging = serializer.save()
                saved_obj = saved_combined_tagging
                return Response(saved_obj, status=status.HTTP_201_CREATED)


class GamesessionView(APIView):
    """
    API View that handles gamesessions
    """
    serializer_class = GamesessionSerializer

    def get_queryset(self):
        gamesessions = Gamesession.objects.all()
        return gamesessions

    def get(self, request, *args, **kwargs):
        gamesession = self.get_queryset().filter(id=2015703320)
        serializer = GamesessionSerializer(gamesession, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gamesession = request.data.get_queryset()
        serializer = GamesessionSerializer(data=gamesession)
        saved_gamesession = None
        while saved_gamesession is None:
            if serializer.is_valid(raise_exception=True):
                saved_gamesession = serializer.save()
        return Response(saved_gamesession)


class GameroundView(APIView):
    """
    API endpoint that allows gamerounds to be viewed or edited
    """

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        gameround = Gameround.objects.all().filter(id=2015691768)
        serializer = GameroundSerializer(gameround, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gameround = request.data.get_queryset()
        saved_gameround = None
        while saved_gameround is None:
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
        taggings = Tagging.objects.all()
        return taggings

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        gametype = Gametype.objects.all().filter(name="imageLabeler")
        if gametype == "TagATag":
            tag = None
            while tag is None:
                random_idx = random.randint(0, Tag.objects.count() - 1)
                tag = Tagging.objects.all().filter(id=random_idx)
                serializer = TaggingSerializer(tag, many=True)
                return Response(serializer.data)
        else:
            tagging = self.get_queryset().filter(resource=9463)
            serializer = HighestTagCountSerializer(tagging, many=True)
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
        tags = Tag.objects.all()
        # serializer = TagSerializer(tags, many=True)
        return tags

    def get(self, request, *args, **kwargs):
        tag = self.get_queryset().filter(language="fr")
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
    serializer_class = TabooTagSerializer

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        resource = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        serializer = ResourceSerializer(resource, many=True)
        return Response({
            'resource and tags to combine': serializer.data
        })


class GameResourceViewPicture(APIView):
    """
    API view to handle resources
    """
    serializer_class = ResourceSerializer
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        resource = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        serializer = ResourceSerializer(resource, many=True)
        return Response({
            'resource and tags to combine': serializer.data
        })


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
