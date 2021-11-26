from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from frontend.models import *
from frontend.serializers import *


# TODO: Alternatively try one APIView per game (1 game: 1 class)? would that work?

class GametypeView(APIView):
    """
    API View that handles retrieving the correct type of a game
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


class TaggingView(APIView):
    """
    API View to do everything to do with taggings
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

    def check_tag_exists(self, request, tagging, format=None):
        """
        Checks if another tagging string for the same resource has been added before, which is the same as the entered string
        :return:
        """
        tagging_to_check = self.get_tagging(tagging)
        serializer = TaggingSerializer(tagging_to_check)
        if Tagging.objects.filter(tag=tagging_to_check).exists():
            pass

    def put(self, request, pk, format=None):
        """
        saves the tagging to the DB
        :param request:
        :param pk:
        :param format:
        :return:
        """
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


class TagView(APIView):
    """
    API View that deals with tags
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
    """
    API view to
    """
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



