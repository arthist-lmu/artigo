import random

import time
from datetime import datetime, timedelta

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
        current_gameround = Gameround.objects.all().filter(taggings__resource_id=random_resource_id).order_by("?").first()
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

        gametype = Gametype.objects.all().get(name="imageLabeler")
        gametype_serializer = GametypeSerializer(gametype)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(user_id=current_user_id,
                                                 gametype=gametype,
                                                 created=datetime.now()
                                                 )

        random_resource = Resource.objects.all().order_by('?').first()
        resource_serializer = ResourceSerializer(random_resource)

        gameround = Gameround.objects.create(user_id=current_user_id,
                                             gamesession=gamesession,
                                             created=datetime.now(),
                                             score=current_score
                                             )
        gameround_serializer = GameroundSerializer(gameround)

        return Response({'gametype': gametype_serializer.data,
                         'resource': resource_serializer.data,
                         'gameround': gameround_serializer.data,
                         })
        # else:
        #     return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    def post(self, request, *args, **kwargs):
        controller = GameViewController()
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk
        gameround = request.GET.get('gameround', '')
        random_resource = request.GET.get('resource', '')
        created = datetime.now()
        score = 0
        origin = ''
        saved_tagging = None
        # name = request.POST['name']
        name = request.POST.get('name', '')
        language = request.POST.get('language', '')

        # A previously played gameround for this resource is coordinated for Tag verification
        # coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

        # user_input_tag = Tag.objects.create(name=name, language=language)
        # tag_serializer = TagSerializer(user_input_tag)

        tag_serializer = TagSerializer(data=request.data)
        tagging_serializer = TaggingSerializer(data=request.data)

        # if Tagging.objects.all().filter(tag=user_input_tag).exists():
        #     # if tagging like this exists, save tagging anyway and leave tag unchanged
        #     score += 5
        #     user_input_tagging = Tagging.objects.create(user_id=current_user_id,
        #                                                 gameround=gameround,
        #                                                 resource=random_resource,
        #                                                 tag=user_input_tag,
        #                                                 created=created,
        #                                                 score=score,
        #                                                 origin=origin)
        #
        #     tagging_serializer = TaggingSerializer(user_input_tagging)
        #
        #     return Response({'tag and ': tag_serializer.data}, {'tagging': tagging_serializer.data})
        #
        # elif not Tagging.objects.all().filter(tag=user_input_tag).exists():
        #     # save tagging otherwise and del tag?
        #     user_input_tagging = Tagging.objects.create(user_id=current_user_id,
        #                                                 gameround=gameround,
        #                                                 resource=random_resource,
        #                                                 tag=user_input_tag,
        #                                                 created=created,
        #                                                 score=score,
        #                                                 origin=origin)
        #     user_input_tagging.save()
        #     tagging_serializer = TaggingSerializer(user_input_tagging)
        #     return Response({'tagging only': tagging_serializer.data})
        #
        # tagging_serializer = TaggingSerializer(data=request.data)
        # if tagging_serializer.is_valid(raise_exception=True):
        #     saved_tagging = Tagging.objects.create(user_id=current_user_id,
        #                                            gameround=gameround,
        #                                            resource=random_resource,
        #                                            tag=user_input_tag,
        #                                            created=created,
        #                                            score=score,
        #                                            origin=origin)
        #     saved_tagging.save(saved_tagging)
        #     tagging_serializer = TaggingSerializer(saved_tagging)
        #     return Response({'status': 'success', 'tagging': tagging_serializer.data}, status=status.HTTP_200_OK)
        #
        # if saved_tagging is None:
        #     return Response({'tagging': tagging_serializer.data}, status=status.HTTP_204_NO_CONTENT)
        # else:
        #     return Response(saved_tagging, status=status.HTTP_400_BAD_REQUEST)
        if tag_serializer.is_valid(raise_exception=True):
            user_input_tag = Tag.objects.create(name=name, language=language)
            tag_serializer.save(user_input_tag)
            user_input_tagging = Tagging.objects.create(user_id=current_user_id,
                                                        gameround=gameround,
                                                        resource=random_resource,
                                                        created=created,
                                                        score=score,
                                                        origin=origin)
            tagging_serializer.save(user_input_tagging)
            return Response({'tagging': tagging_serializer}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

        gametype = Gametype.objects.all().get(name="imageLabeler_Taboo")
        gametype_serializer = GametypeSerializer(gametype)

        resource_suggestions = Resource.objects.all().order_by('?').first()
        resource_serializer = TabooTagSerializer(resource_suggestions)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(
            # id=controller.generate_random_id(Gamesession),
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            # id=controller.generate_random_id(Gameround),
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )
        gameround_serializer = GameroundSerializer(gameround)

        return Response({'gametype': gametype_serializer.data,
                         'resourceand taboo input': resource_serializer.data,
                         'gameround': gameround_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        controller = GameViewController()
        saved_tag = None
        current_user = CustomUserSerializer(data=request.user)  # user instance
        tag_serializer = TagSerializer(data=request.data)

        random_resource = request.data('resource')
        # A previously played gameround for this resource is coordinated for Tag verification
        coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

        if tag_serializer.is_valid(raise_exception=True):
            saved_tag = Tag.objects.create(# id=controller.generate_random_id(Tag),
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
        gametype = Gametype.objects.all().get(name="imageAndTagLabeler")
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
            # id=controller.generate_random_id(Gamesession),
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            # id=controller.generate_random_id(Gameround),
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )
        gameround_serializer = GameroundSerializer(gameround)

        return Response({'gametype': gametype_serializer.data,
                         'tag': tagging_serializer.data,
                         'resourceand and suggestions': suggestions_serializer.data,
                         'gameround': gameround_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        saved_tagging = None

        serializer = TaggingSerializer(data=request.data)

        random_resource = request.data('resource')
        # A previously played gameround for this resource is coordinated for Tag verification
        coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

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

        gametype = Gametype.objects.all().get(name="Combino")
        gametype_serializer = GametypeSerializer(gametype)

        resource_and_tags = Resource.objects.all().order_by('?').first()
        combination_serializer = CombinoTagsSerializer(resource_and_tags)

        current_score = 0
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        gamesession = Gamesession.objects.create(
            # id=controller.generate_random_id(Gamesession),
            user_id=current_user_id,
            gametype=gametype,
            created=datetime.now()
        )

        gameround = Gameround.objects.create(
            # id=controller.generate_random_id(Gameround),
            user_id=current_user_id,
            gamesession=gamesession,
            created=datetime.now(),
            score=current_score
        )
        gameround_serializer = GameroundSerializer(gameround)

        return Response({'gametype': gametype_serializer.data,
                         'resourceand and tags to combine': combination_serializer.data,
                         'gameround': gameround_serializer.data
                         })

    def post(self, request, *args, **kwargs):
        controller = GameViewController()
        saved_combined_tagging = None

        random_resource = request.data('resource')

        # A previously played gameround for this resource is coordinated for Tag verification
        coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

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

        random_resource = Resource.objects.all().order_by('?').first()
        resource_serializer = ResourceSerializer(random_resource)  # Response is a serialized JSON object
        random_resource_id = random_resource.id   # id of the random Resource for the game round
        gameround = Gameround.objects.all().filter(taggings__resource_id=random_resource_id).order_by("?").first()
        gameround_serializer = GameroundSerializer(gameround)

        return Response({
            'resource to coordinate': resource_serializer.data,
            'gameround': gameround_serializer.data,
        })

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
        """Retrieves a random Tag"""
        # tagging = Tagging.objects.all().order_by('?').first()
        # tagging_serializer = TaggingSerializer(tagging)
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk
        score = 0

        gamesession = Gamesession.objects.create(user_id=current_user_id,
                                                 gametype=Gametype.objects.all().order_by('?').first(),
                                                 created=datetime.now())
        gameround = Gameround.objects.create(user_id=current_user_id,
                                             gamesession=gamesession,
                                             created=datetime.now(),
                                             score=score)
        random_resource = Resource.objects.all().order_by('?').first()

        # A previously played gameround for this resource is coordinated for Tag verification
        controller = GameViewController()
        coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

        origin = ''
        user_input_tag = Tag.objects.create(name='new tag obj', language='de')
        tag_serializer = TagSerializer(user_input_tag)

        if Tagging.objects.all().filter(tag=user_input_tag).exists():
            # if tagging like this exists, save tagging anyway and leave tag unchanged
            score += 5
            user_input_tagging = Tagging.objects.create(user_id=current_user_id,
                                                        gameround=gameround,
                                                        resource=random_resource,
                                                        tag=user_input_tag,
                                                        created=datetime.now(),
                                                        score=score,
                                                        origin=origin)

            tagging_serializer = TaggingSerializer(user_input_tagging)

            return Response({'tag and ': tag_serializer.data}, {'tagging': tagging_serializer.data})

        elif not Tagging.objects.all().filter(tag=user_input_tag).exists():
            # save tagging otherwise and del tag
            user_input_tagging = Tagging.objects.create(user_id=current_user_id,
                                                        gameround=gameround,
                                                        resource=random_resource,
                                                        tag=user_input_tag,
                                                        created=datetime.now(),
                                                        score=score,
                                                        origin=origin)
            user_input_tagging.save()
            tagging_serializer = TaggingSerializer(user_input_tagging)
            # user_input_tag.delete()
            return Response({'tagging only': tagging_serializer.data})

    def post(self, request, *args, **kwargs):
        if not isinstance(request.user, CustomUser):
            current_user_id = 1
        else:
            current_user_id = request.user.pk

        tagging_serializer = TaggingSerializer(data=request.data)

        gamesession = Gamesession.objects.create(user_id=current_user_id,
                                                 gametype=Gametype.objects.all().order_by('?').first(),
                                                 created=datetime.now())

        gameround = Gameround.objects.create(user_id=current_user_id,
                                             gamesession=gamesession,
                                             created=datetime.now(),
                                             score=current_score)

        random_resource = Resource.objects.all().order_by('?').first()

        # A previously played gameround for this resource is coordinated for Tag verification
        # coordinated_gameround = controller.get_gameround_matching_resource(random_resource.id)

        score = 0
        origin = ''

        tagging_serializer = TaggingSerializer(saved_tagging)

        if tagging_serializer.is_valid():
            saved_tagging = Tagging.objects.create(user_id=current_user_id,
                                                   gameround=gameround,
                                                   resource=random_resource,
                                                   tag=Tag.objects.create(name=request.POST.get("name"),
                                                                          language=request.POST.get("language")),
                                                   created=datetime.now(),
                                                   score=score,
                                                   origin=origin)
            tagging_serializer.save(saved_tagging)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    """
    API endpoint that allows tags to be viewed or edited
    """

    def get(self, request, *args, **kwargs):
        tag = Tag.objects.all().order_by('?').first()
        tag_serializer = TagSerializer(tag)
        return Response(tag_serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        # tag_input = Tag.objects.create(name=request.POST.get("name"), language=request.POST.get("language"))
        if serializer.is_valid(raise_exception=True):
            serializer.save(tag=request.data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
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
