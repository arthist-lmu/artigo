import random

import time

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

    def get_custom_tags(self):
        tag_count = None
        pass

    def get_gameround(self):
        pass

    def get_gamesession(self):
        pass

    def get_time_created(self):
        pass

    def get_resource(self):
        pass

    def calculate_score(self, tagging_to_check, gameround):
        # returns JSON Object // HTTP Status code
        score_to_save = None
        # 'Matching' here: match played round with a previously played round (25 p) and with entire DB->Tagging(5p)

        self.coordinate_players(gameround)

        return Response(saved_tagging, status=status.HTTP_201_CREATED)

    def check_tag_exists(self, tagging_to_check):
        """
        Checks if another tagging string for the same resource has been added before, which is the same as the entered string
        :return:
        """
        saved_tagging = None
        saved_tag = None
        # TODO: figure out if serializers neccessary here
        tagging_serializer = TaggingSerializer(tagging_to_check)
        tag_serializer = TagSerializer()
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

    def coordinate_players(self, current_gameround):
        pass

    def start_game(self, gametype, gameround):

        self.coordinate_players(gameround)


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

    # renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    # TODO: USE LATER!!!!
    # renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        """

        :return:
        """
        obj = None
        resource = None
        gameround = None
        gamesession = None
        random_resource_idx = None

        while obj is None:
            if obj == resource:
                while resource is None:
                    while random_resource_idx is None:
                        while not Resource.objects.all().filter(id=random_resource_idx).exists():
                            random_number = random.randint(0, Resource.objects.count() - 1)
                            if not Resource.objects.all().filter(id=random_number).exists():
                                random_number_alternative = random.randint(0, Resource.objects.count() - 1)
                                if Resource.objects.all().filter(id=random_number_alternative).exists():
                                    random_resource_idx = random_number_alternative
                                else:
                                    random_resource_idx = random_number
                        resource = Resource.objects.all().filter(id=random_resource_idx)
                    obj = resource

            elif obj == gamesession:
                while gamesession is None:
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    gameround = Gameround.objects.none()
                    obj = gameround

        return obj

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        artigo_gametype = "imageLabeler"
        gametype = GametypeView()
        gametype.get_queryset()
        # TODO: Build timer in!!!
        model = request.GET.get("model")
        resource_serializer = None
        gameround_serializer = None
        gamesession_serializer = None
        # TODO: find way to assign what model is?
        model = "Resource"  # For testing purposes only!

        while resource_serializer is None:
            # if model == "Resource":
            resource = self.get_queryset()
            resource_serializer = ResourceSerializer(resource, many=True)
        while gameround_serializer is None:
            # elif model == "Gameround":
            gameround = Gameround.objects.none()
            gameround_serializer = GameroundSerializer(gameround, many=True)
        while gamesession_serializer is None:
            # elif model == "Gamesession":
            gamesession = Gamesession.objects.none()
            gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        # TODO: only save if 5 rounds have been played! Tags/Taggings can be saved - find a way!
        return Response({'resource': resource_serializer.data,
                         'gameround': gameround_serializer.data,
                         'gamesession': gamesession_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        saved_tagging = None
        serializer = TaggingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'tagging': serializer.data}, status=status.HTTP_201_CREATED)
        if saved_tagging is None:
            return Response({'tagging': serializer.data}, status=status.HTTP_201_CREATED)
            # return Response(saved_obj, status=status.HTTP_201_CREATED)

        return Response(saved_tagging, status=status.HTTP_400_BAD_REQUEST)
        # controller = GameViewController()
        # saved_tagging = None
        # saved_tag = None
        # saved_obj = None
        #
        # # user object - remains the same over the session
        # user_object = request.user
        #
        # model = request.GET.get("model") # coordinate using GameController
        # # condition checks if the tag in the request exists and then sends it to proper POST
        # # if controller.check_tag_exists(request.GET.get("name")) == Tag():
        # #     model = "Tag"
        # # else:
        # #     model = "Tagging"
        #
        # # TODO: Resource id has to be sent with tag/tagging!
        # if model == "Tagging":
        #     # TODO: test & modify if necessary
        #     tagging = ResourceWithTaggingsSerializer(data=request.data)
        #     while saved_tagging is None:
        #         serializer = ResourceWithTaggingsSerializer(data=tagging)
        #         if serializer.is_valid(raise_exception=True):
        #             saved_tagging = serializer.save()
        #             saved_obj = saved_tagging
        #             return Response(saved_obj, status=status.HTTP_201_CREATED)
        #
        # elif model == "Tag":
        #     tag = ResourceWithTagsSerializer(data=request.data)
        #     while saved_tag is None:
        #         serializer = ResourceWithTagsSerializer(data=tag)
        #         if serializer.is_valid(raise_exception=True):
        #             saved_tag = serializer.save()
        #             saved_obj = saved_tag
        #             return Response(saved_obj, status=status.HTTP_201_CREATED)
        #
        # return Response(saved_obj, status=status.HTTP_400_BAD_REQUEST)


class ARTigoTabooGameView(APIView):
    """
    API View that retrieves the ARTigo Taboo game,
    retrieves an empty game session to be filled with the necessary data and sent back to the server
    retrieves a random resource per round along with the taboo tags for the respective resource
    allows users to post tags that are verified and saved accordingly to either the Tag or Tagging table
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    controller = GameViewController()

    def get_queryset(self):
        """

        :return:
        """
        obj = None
        resource = None
        resources = Resource.objects.all()
        artigo_taboo_gametype = None
        gameround = None
        gamesession = None
        random_resource_idx = None

        while obj is None:
            if obj == resource:
                while resource is None:
                    while random_resource_idx is None:
                        while not resources.filter(id=random_resource_idx).exists():
                            random_number = random.randint(0, resources.count() - 1)
                            if not resources.filter(id=random_number).exists():
                                random_number_alternative = random.randint(0, resources.count() - 1)
                                if resources.filter(id=random_number_alternative).exists():
                                    random_resource_idx = random_number_alternative
                                else:
                                    random_resource_idx = random_number
                        resource = resources.filter(id=random_resource_idx)
                    obj = resource

            elif obj == artigo_taboo_gametype:
                while artigo_taboo_gametype is None:
                    artigo_taboo_gametype = Gametype.objects.all().filter(name="imageLabeler_Taboo")
                    obj = artigo_taboo_gametype

            elif obj == gamesession:
                while gamesession is None:
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    gameround = Gameround.objects.none()
                    obj = gameround

        return obj

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        model = request.GET.get("model")
        resource_serializer = None
        gameround_serializer = None
        gamesession_serializer = None
        # TODO: find way to assign what model is?
        model = "Resource"  # For testing purposes only!
        while resource_serializer is None:
            # if model == "Resource":
            # gametype = self.get_queryset()
            # serializer = GametypeSerializer(gametype, many=True)
            resource = self.get_queryset()
            resource_serializer = TabooTagSerializer(resource, many=True)
        while gameround_serializer is None:
            # elif model == "Gameround":
            # TODO: find a good way to send an empty gameround/session object
            #  to be filled while game is being played
            gameround = Gameround.objects.none()
            gameround_serializer = GameroundSerializer(gameround, many=True)
        while gamesession_serializer is None:
            # elif model == "Gamesession":
            # TODO: find a good way to send an empty gameround/session object
            #  to be filled while game is being played
            gamesession = Gamesession.objects.none()
            gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({'resource and taboo input': resource_serializer.data,
                         'gameround': gameround_serializer.data,
                         'gamesession': gamesession_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        controller = GameViewController()
        saved_gameround = None
        saved_gamesession = None
        saved_tagging = None
        saved_tag = None
        saved_obj = None

        model = request.GET.get("model")
        model = "Tagging"

        # if controller.check_tag_exists(request.GET.get("name")) == Tag():
        #     model = "Tag"
        # else:
        #     model = "Tagging"

        # TODO: Resource id has to be sent with tag/tagging!
        if model == "Tagging":
            # TODO: test & modify if necessary
            tagging = ResourceWithTaggingsSerializer(data=request.data)
            while saved_tagging is None:
                serializer = ResourceWithTaggingsSerializer(data=tagging)
                if serializer.is_valid(raise_exception=True):
                    saved_tagging = serializer.save()
                    saved_obj = saved_tagging
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        elif model == "Tag":
            # TODO: add condition to only save to tag if condition met
            tag = ResourceWithTagsSerializer(data=request.data)
            while saved_tag is None:
                serializer = ResourceWithTagsSerializer(data=tag)
                if serializer.is_valid(raise_exception=True):
                    saved_tag = serializer.save()
                    saved_obj = saved_tag
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        return Response(saved_obj, status=status.HTTP_400_BAD_REQUEST)


class TagATagGameView(APIView):
    """
    API endpoint that retrieves the Tag a Tag game
    """

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        gametype = Gametype.objects.all().filter(name="imageAndTagLabeler")
        # TODO: See that logic is here and not in get_queryset()

        # random tag to be labeled in combination with the question and picture
        # tag = self.get_queryset()
        resource_suggestions = Resource.objects.order_by('?').first()
        suggestions_serializer = SuggestionsSerializer(resource_suggestions, many=True)

        # tag = Tagging.objects.all().filter(resource=resource_suggestions)
        tag = Tagging.objects.order_by('?').first()
        tagging_serializer = TaggingSerializer(tag, many=True)

        # TODO: ask again if empty object neccessary
        gameround = Gameround.objects.none()
        gameround_serializer = GameroundSerializer(gameround, many=True)

        gamesession = Gamesession.objects.none()
        gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({
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

    def get_queryset(self):
        obj = None
        resource = None
        gameround = None
        gamesession = None
        random_resource_idx = None

        while obj is None:

            if obj == resource:
                while resource is None:
                    while random_resource_idx is None:
                        while not Resource.objects.all().filter(id=random_resource_idx).exists():
                            random_number = random.randint(0, Resource.objects.count() - 1)
                            if not Resource.objects.all().filter(id=random_number).exists():
                                random_number_alternative = random.randint(0, Resource.objects.count() - 1)
                                if Resource.objects.all().filter(id=random_number_alternative).exists():
                                    random_resource_idx = random_number_alternative
                                else:
                                    random_resource_idx = random_number
                        resource = Resource.objects.all().filter(id=random_resource_idx)
                    obj = resource

            elif obj == gamesession:
                while gamesession is None:
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    gameround = Gameround.objects.none()
                    obj = gameround

        return obj

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        gametype = Gametype.objects.all().filter(name="Combino")
        # TODO: See that it does not return an empty object!
        combination_serializer = None
        resource_and_tags = None
        gameround_serializer = None
        gamesession_serializer = None

        while combination_serializer is None:
            # random resource with tags to be combined
            while resource_and_tags is None:
                resource_and_tags = self.get_queryset()
                combination_serializer = CombinoTagsSerializer(resource_and_tags, many=True)
        while gameround_serializer is None:
            gameround = Gameround.objects.none()
            gameround_serializer = GameroundSerializer(gameround, many=True)
        while gamesession_serializer is None:
            gamesession = Gamesession.objects.none()
            gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({
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
        gamesessions = Gamesession.objects.all().filter(id=2015703320)
        return gamesessions

    def get(self, request, *args, **kwargs):
        gamesession = self.get_queryset()
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
        taggings = Tagging.objects.all().filter(resource=9463)
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
    serializer_class = TabooTagSerializer

    def get_queryset(self):
        resource = None
        random_resource_idx = None
        while resource is None:
            while resource is None:
                while random_resource_idx is None:
                    while not Resource.objects.all().filter(id=random_resource_idx).exists():
                        random_number = random.randint(0, Resource.objects.count() - 1)
                        if not Resource.objects.all().filter(id=random_number).exists():
                            random_number_alternative = random.randint(0, Resource.objects.count() - 1)
                            if Resource.objects.all().filter(id=random_number_alternative).exists():
                                random_resource_idx = random_number_alternative
                            else:
                                random_resource_idx = random_number
                    resource = Resource.objects.all().filter(id=random_resource_idx)
        return resource

    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = TabooTagSerializer(resource, many=True)
        return Response({
            'resource and tags to combine': serializer.data
        })


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
