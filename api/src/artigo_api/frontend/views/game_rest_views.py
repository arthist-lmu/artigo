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
    def generate_random_id(self, MyModel):
        """ Picks a random id for an object to be created"""
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

    def get_random_object(self, MyModel):
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

    def get_resource(self):
        random_resource_id = self.get_random_object(Resource)
        current_resource = Resource.objects.all().filter(id=random_resource_id)
        resource_serializer = ResourceSerializer(current_resource, many=True)
        data = {'resource': resource_serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def get_gameround_matching_resource(self, random_resource):
        """Checks if a previously played game round exists for a randomly chosen resource"""
        # TODO: decide whether to do the coordination here or in the other method!
        current_gameround = Gameround.objects.all().filter(ressource__in=random_resource).order_by('?').first()

        if current_gameround.exists():
            gameround_serializer = GameroundSerializer(current_gameround)
            data = {'gameround': gameround_serializer.data}
            return Response(data, status=status.HTTP_200_OK)

    def timer(self, start):
        """Start a new timer as soon as a gameround has been selected"""
        start_time = start
        elapsed_time = None
        if start_time is not None:
            start_time = time.perf_counter()
        """Stop the timer, and return the elapsed time"""
        if start_time is None:
            elapsed_time = time.perf_counter() - start_time
        return elapsed_time

    def get_gamesession(self):
        """Retrieves a randomly chosen gamesession object"""
        current_gamesession = Gamesession.objects.all().order_by('?').first()
        gamesession_serializer = GamesessionSerializer(current_gamesession)
        data = {'gameround': gamesession_serializer.data}
        return Response(data, status=status.HTTP_200_OK)

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
        random_resource = Resource.objects.all().filter(id=controller.get_random_object(Resource))
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

        resource_suggestions = Resource.objects.all().filter(id=controller.get_random_object(Resource))
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

        resource_suggestions = Resource.objects.all().filter(id=controller.get_random_object(Resource))
        suggestions_serializer = SuggestionsSerializer(resource_suggestions, many=True)

        tag = Tagging.objects.filter(resource__in=resource_suggestions).order_by('?').first()
        tagging_serializer = TaggingSerializer(tag)

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

    def get(self, request, *args, **kwargs):
        gamesession = Gamesession.objects.all().order_by('?').first()
        serializer = GamesessionSerializer(gamesession)
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
        # TODO: Finish this concept & move it to controller!
        controller = GameViewController()
        random_resource = controller.get_resource() # Response is a JSON object
        random_resource_id = random_resource.get(random_resource.id) # id of the random Resource for the game round
        gameround = Gameround.objects.all().filter(taggings__resource_id=random_resource_id).order_by("?").first()
        gameround_serializer = GameroundSerializer(gameround)
        return Response(gameround_serializer.data)

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

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        # TODO: FIX THIS WEIRD ISSUE [{}, {}]
        # tagging = self.get_queryset().values().latest('created')
        tagging = Tagging.objects.all().order_by('?').first()
        serializer = TaggingSerializer(tagging)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        tag = Tag.objects.all().filter(id=controller.get_random_object(Tag))
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
    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        resource = Resource.objects.all().filter(id=controller.get_random_id(Resource))
        serializer = ResourceSerializer(resource, many=True)
        return Response({
            'resource': serializer.data
        })


class GameResourceViewPicture(APIView):
    """
    API view to handle resources
    """
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        controller = GameViewController()
        resource = Resource.objects.all().filter(id=controller.pick_random_object(Resource))
        serializer = ResourceSerializer(resource, many=True)
        return Response({
            'resource and tags to combine': serializer.data
        })
