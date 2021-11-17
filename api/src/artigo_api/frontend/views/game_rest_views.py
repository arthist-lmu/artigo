from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from frontend.models import Tagging, Tag


class TaggingsView(APIView):
    """
    View to list all taggings so far
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
        Returns all taggings
        :param request:
        :param format:
        :return:
        """
        tags = [tags.tag for tags in Tag.objects.all()]
        return Response(tags)

