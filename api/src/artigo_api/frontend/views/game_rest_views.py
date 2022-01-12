import random

import time

from rest_framework import status
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

    def check_tag_exists(self):
        """
        Checks if another tagging string for the same resource has been added before, which is the same as the entered string
        :return:
        """
        tagging_to_check = None
        tagging = None

        tagging_to_check.get_queryset(tagging)
        serializer = TaggingSerializer(tagging_to_check)
        if Tagging.objects.filter(tag=tagging_to_check).exists():
            pass

    def calculate_score(self):
        pass

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

    def start_game(self):
        pass

    def coordinate_players(self):
        pass


class MasterClass(APIView):

    def dispatch(self, request, *args, **kwargs):
        # TODO: Review and maybe rewrite with my logic
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


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
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    controller = GameViewController()

    def get_serializer_class(self):
        YOUR_DEFAULT_SERIALIZER = GametypeSerializer
        YOUR_SERIALIZER_1 = GamesessionSerializer
        YOUR_SERIALIZER_2 = GameroundSerializer
        YOUR_SERIALIZER_3 = ResourceSerializer
        YOUR_SERIALIZER_4 = TagSerializer
        YOUR_SERIALIZER_5 = TaggingSerializer

        if self.request.method == 'POST':
            return YOUR_SERIALIZER_4 and YOUR_SERIALIZER_5 and YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2 and YOUR_SERIALIZER_3
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        """

        :return:
        """
        obj = None
        resources = None
        gameround = None
        gamesession = None

        while obj is None:
            if obj == resources:
                while resources is None:
                    random_idx = random.randint(0, Resource.objects.count() - 1)
                    resources = Resource.objects.all().filter(id=random_idx)
                    obj = resources

            elif obj == gamesession:
                while gamesession is None:
                    # TODO: figure out how to send empty gamesession
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    # TODO: figure out how to send empty gameround
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
                # TODO: find a good way to send an empty gameround object
                #  to be filled while game is being played
                gameround = Gameround.objects.none()
                gameround_serializer = GameroundSerializer(gameround, many=True)
        while gamesession_serializer is None:
            # elif model == "Gamesession":
                # TODO: find a good way to send an empty gamesession object
                #  to be filled while game is being played
                gamesession = Gamesession.objects.none()
                gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({'resource': resource_serializer.data,
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
        saved_gameround = None
        saved_gamesession = None
        saved_tagging = None
        saved_tag = None
        saved_obj = None

        model = request.GET.get("model")
        model = "Tagging"

        if model == "Gameround":
            # gameround = request.data.get_queryset()
            gameround = GameroundSerializer(data=request.data)
            while saved_gameround is None:
                serializer = GameroundSerializer(data=gameround)
                if serializer.is_valid(raise_exception=True):
                    saved_gameround = serializer.save()
                    saved_obj = saved_gameround
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        elif model == "Gamesession":
            # TODO: only save if 5 rounds have been played?! or always?
            gamesession = request.data.get_queryset()
            while saved_gamesession is None:
                serializer = GamesessionSerializer(data=gamesession)
                if serializer.is_valid(raise_exception=True):
                    saved_gamesession = serializer.save()
                    saved_obj = saved_gamesession
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        # TODO: Resource id has to be sent with tag/tagging!
        elif model == "Tagging":
            # TODO: test & modify if necessary
            # tagging = request.data.get_queryset()
            tagging = serializer.ResourceWithTaggingsSerializer(data=request.data)
            while saved_tagging is None:
                serializer = ResourceWithTaggingsSerializer(data=tagging)
                if serializer.is_valid(raise_exception=True):
                    saved_tagging = serializer.save()
                    saved_obj = saved_tagging
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        elif model == "Tag":
            # TODO: add condition to only save to tag if condition met
            # tag = request.data.get_queryset()
            tag = serializer.ResourceWithTagsSerializer(data=request.data)
            while saved_tag is None:
                serializer = ResourceWithTagsSerializer(data=tag)
                if serializer.is_valid(raise_exception=True):
                    saved_tag = serializer.save()
                    saved_obj = saved_tag
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        return Response(saved_obj, status=status.HTTP_400_BAD_REQUEST)


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
        resources = None
        artigo_taboo_gametype = None
        gameround = None
        gamesession = None

        while obj is None:
            if obj == resources:
                while resources is None:
                    random_idx = random.randint(0, Resource.objects.count() - 1)
                    resources = Resource.objects.all().filter(id=random_idx)
                    obj = resources

            elif obj == artigo_taboo_gametype:
                while artigo_taboo_gametype is None:
                    artigo_taboo_gametype = Gametype.objects.all().filter(name="imageLabeler_Taboo")
                    obj = artigo_taboo_gametype

            elif obj == gamesession:
                while gamesession is None:
                    # TODO: figure out how to send empty gamesession
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    # TODO: figure out how to send empty gameround
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
        saved_gameround = None
        saved_gamesession = None
        saved_tagging = None
        saved_tag = None
        saved_obj = None

        model = request.GET.get("model")
        model = "Tagging"

        if model == "Gameround":
            # gameround = request.data.get_queryset()
            gameround = GameroundSerializer(data=request.data)
            while saved_gameround is None:
                serializer = GameroundSerializer(data=gameround)
                if serializer.is_valid(raise_exception=True):
                    saved_gameround = serializer.save()
                    saved_obj = saved_gameround
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        elif model == "Gamesession":
            # TODO: only save if 5 rounds have been played?! or always?
            gamesession = request.data.get_queryset()
            while saved_gamesession is None:
                serializer = GamesessionSerializer(data=gamesession)
                if serializer.is_valid(raise_exception=True):
                    saved_gamesession = serializer.save()
                    saved_obj = saved_gamesession
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        # TODO: Resource id has to be sent with tag/tagging!
        elif model == "Tagging":
            # TODO: test & modify if necessary
            # tagging = request.data.get_queryset()
            tagging = serializer.ResourceWithTaggingsSerializer(data=request.data)
            while saved_tagging is None:
                serializer = ResourceWithTaggingsSerializer(data=tagging)
                if serializer.is_valid(raise_exception=True):
                    saved_tagging = serializer.save()
                    saved_obj = saved_tagging
                    return Response(saved_obj, status=status.HTTP_201_CREATED)

        elif model == "Tag":
            # TODO: add condition to only save to tag if condition met
            # tag = request.data.get_queryset()
            tag = serializer.ResourceWithTagsSerializer(data=request.data)
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

    def get_serializer_class(self):
        YOUR_DEFAULT_SERIALIZER = GametypeSerializer
        YOUR_SERIALIZER_1 = GamesessionSerializer
        YOUR_SERIALIZER_2 = GameroundSerializer
        # returns a Resource and the suggested tags to describe the relationship between random tag and resource
        YOUR_SERIALIZER_3 = SuggestionsSerializer
        YOUR_SERIALIZER_4 = TagSerializer
        YOUR_SERIALIZER_5 = TaggingSerializer

        if self.request.method == 'POST':
            return YOUR_SERIALIZER_4 and YOUR_SERIALIZER_5 and YOUR_SERIALIZER_1
        elif self.request.method == 'GET':
            return YOUR_SERIALIZER_2 and YOUR_SERIALIZER_3
        else:
            return YOUR_DEFAULT_SERIALIZER

    def get_queryset(self):
        """

        :return:
        """
        obj = None
        resources = None
        gameround = None
        gamesession = None

        while obj is None:
            if obj == resources:
                while resources is None:
                    random_idx = random.randint(0, Resource.objects.count() - 1)
                    resources = Resource.objects.all().filter(id=random_idx)
                    obj = resources

            elif obj == gamesession:
                while gamesession is None:
                    # TODO: figure out how to send empty gamesession
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    # TODO: figure out how to send empty gameround
                    gameround = Gameround.objects.none()
                    obj = gameround

        return obj

    def get(self, request, *args, **kwargs):
        """Potential condition for Tag a Tag Tag to be tagged to be returned"""
        gametype = Gametype.objects.all().filter(name="imageAndTagLabeler")
        # TODO: See that it does not return an empty object!
        tag = None
        tag_serializer = None
        suggestions_serializer = None
        resource_suggestions = None
        gamesession_serializer = None
        gameround_serializer = None

        while tag_serializer is None:
            while tag is None:
                # random tag to be labeled in combination with the question and picture
                random_idx = random.randint(0, Tag.objects.count() - 1)
                tag = Tag.objects.all().filter(id=random_idx)
                tag_serializer = TagSerializer(tag, many=True)
        while suggestions_serializer is None:
            while resource_suggestions is None:
                resource_suggestions = self.get_queryset()
                suggestions_serializer = SuggestionsSerializer(resource_suggestions, many=True)
        while gameround_serializer is None:
                # TODO: find a good way to send an empty gameround/session object
                #  to be filled while game is being played
                gameround = Gameround.objects.none()
                gameround_serializer = GameroundSerializer(gameround, many=True)
        while gamesession_serializer is None:
                # TODO: find a good way to send an empty gameround/session object
                #  to be filled while game is being played
                gamesession = Gamesession.objects.none()
                gamesession_serializer = GamesessionSerializer(gamesession, many=True)

        return Response({
            'tag': tag_serializer.data,
            'resource and suggestions': suggestions_serializer.data,
            'gameround': gameround_serializer.data,
            'gamesession': gamesession_serializer.data
        })

    def post(self, request, *args, **kwargs):
        pass


class CombinoGameView(APIView):
    """
    API endpoint that retrieves the Combino game view
    """

    def get_queryset(self):
        obj = None
        resources = None
        gameround = None
        gamesession = None

        while obj is None:

            if obj == resources:
                while resources is None:
                    random_idx = random.randint(0, Resource.objects.count() - 1)
                    resources = Resource.objects.all().filter(id=random_idx)
                    obj = resources

            elif obj == gamesession:
                while gamesession is None:
                    # TODO: figure out how to send empty gamesession
                    gamesession = Gamesession.objects.none()
                    obj = gamesession

            elif obj == gameround:
                while gameround is None:
                    # TODO: figure out how to send empty gameround
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
        pass


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
    serializer_class = CombinoTagsSerializer

    def get_queryset(self):
        resources = None
        while resources is None:
            random_idx = random.randint(0, Resource.objects.count() - 1)
            resources = Resource.objects.all().filter(id=random_idx)
        # TODO: See that a resource is always returned! check that resource not null
        return resources

    def get(self, request, *args, **kwargs):
        resource = self.get_queryset()
        serializer = CombinoTagsSerializer(resource, many=True)
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



