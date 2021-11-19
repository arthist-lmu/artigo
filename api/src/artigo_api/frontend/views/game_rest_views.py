from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from frontend.models import Tagging, Tag


# TODO: Alternatively try one APIView per game (1 game: 1 class)? would that work?


class TaggingsView(APIView):
    """
    View to do everything to do with taggings
    """

    def get_taggings(self, request, format=None):
        """
        Returns all taggings
        :param request:
        :param format:
        :return:
        """
        taggings = [tagging.tag for tagging in Tagging.objects.all()]
        return Response(taggings)

    def save_to_tagging(self, request, format=None):
        """
        Saves a tagging into the Tagging table
        :param request:
        :param format:
        :return:
        """


class TagView(APIView):
    def save_to_tag(self, request, format=None):
        """
        Saves a tag to the Tag table
        :param request:
        :param format:
        :return:
        """

    def get_tags(self, request, format=None):
        """
        Returns all tags
        :param request:
        :param format:
        :return:
        """
        tags = [tags.tag for tags in Tag.objects.all()]
        return Response(tags)

    def get_custom_tags(self, request, number):
        """
        Retrieves a custom number of tags - for ARTigo taboo or Tag a Tag
        :param request:
        :param number: number of tags to be retrieved (1 for Tag a Tag, 5-10 for ARTigo Taboo)
        :return:
        """


class CombinoView(APIView):
    """
    View with methods for Combino game
    """
    def get_combino_tags(self, request):
        """
        Retrieves tags to be combined during a round of Combino
        :param request:
        :return:
        """
        # tagging_to_combine = [tagging.tag for tagging in Tagging.objects.all()]

        tagging_to_combine = []
        for tagging in Tagging.objects.raw('SELECT tag FROM artigo_api_Tagging WHERE COUNT(tag) > 5'):
            tagging_to_combine.append(tagging)
        return Response(tagging_to_combine)

    def save_combined_tags(self, request):
        """
        Saves tags combined tags to the CombinedTagging table/model
        :param request:
        :return:
        """

