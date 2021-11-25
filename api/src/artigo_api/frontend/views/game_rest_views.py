from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from frontend.models import *
from frontend.serializers import *


# TODO: Alternatively try one APIView per game (1 game: 1 class)? would that work?

class GametypeViews(APIView):
    """
    View that handles retrieving the correct type of a game &co
    """
    serializer_class = GametypeSerializer

    def get_gametype(self):
        gametypes = Gametype.objects.all()
        return gametypes

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        gametype = self.get_gametype()
        serializer = GametypeSerializer(gametype)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        gametype = self.get_gametype(pk)
        serializer = GametypeSerializer(gametype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        gametype = self.get_gametype(pk)
        gametype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaggingsView(APIView):
    """
    View to do everything to do with taggings
    """
    serializer_class = TaggingSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def get_tagging(self):
        """
        Returns all taggings
        :param request:
        :param format:
        :return:
        """
        taggings = Tagging.objects.all()
        return taggings

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        tagging = self.get_tagging()
        serializer = TaggingSerializer(tagging)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tagging = self.get_tagging(pk)
        serializer = TaggingSerializer(tagging, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tagging = self.get_tagging(pk)
        tagging.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def save_to_tagging(self, request, format=None):
        """
        Saves a tagging into the Tagging table
        :param request:
        :param format:
        :return:
        """


class TagView(APIView):
    """
    APIView class that deals with tags
    """
    serializer_class = TagSerializer

    def get_tag(self, request, format=None):
        """
        Returns all tags
        :param request:
        :param format:
        :return:
        """
        tags = Tag.objects.all()
        return tags

    @method_decorator(cache_page(60 * 60 * 2))
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

    def save_to_tag(self, request, format=None):
        """
        Saves a tag to the Tag table
        :param request:
        :param format:
        :return:
        """
        pass

    def get_custom_tags(self, request, number):
        """
        Retrieves a custom number of tags - for ARTigo taboo or Tag a Tag
        :param request:
        :param number: number of tags to be retrieved (1 for Tag a Tag, 5-10 for ARTigo Taboo)
        :return:
        """
        pass


class GameResourceView(APIView):
    serializer_class = ResourceSerializer

    def get_resource(self, request, format=None):
        """
        Returns all tags
        :param request:
        :param format:
        :return:
        """
        resources = Resource.objects.all()
        return resources

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        resource = self.get_resource()
        serializer = ResourceSerializer(resource)
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

    def score(self, request):
        pass


# class CombinoView(APIView):
#     """
#     View with methods for Combino game
#     """
#     def get_combino_tags(self, request):
#         """
#         Retrieves tags to be combined during a round of Combino
#         :param request:
#         :return:
#         """
#         # tagging_to_combine = [tagging.tag for tagging in Tagging.objects.all()]
#
#         tagging_to_combine = []
#         for tagging in Tagging.objects.raw('SELECT tag FROM artigo_api_Tagging WHERE COUNT(tag) > 5'):
#             tagging_to_combine.append(tagging)
#         return Response(tagging_to_combine)
#
#     def save_combined_tags(self, request):
#         """
#         Saves tags combined tags to the CombinedTagging table/model
#         :param request:
#         :return:
#         """

