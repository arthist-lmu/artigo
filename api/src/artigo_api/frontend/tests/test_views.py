import pytest

from django.test import TestCase
from rest_framework import response

from frontend.models import *
from frontend.serializers import *
from frontend.views import *


class GameViewControllerTests(TestCase):
    pass


class GameTypeViewTests(TestCase):

    def test_get_queryset(self):
        self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.Response, 200)
        self.assertEqual(len(response.responses), len(Gametype.objects.all()))

    def test_get(self):
        pass


class ARTigoGameViewTests(TestCase):

    def test_get(self):
        pass

    def test_post(self):
        pass


class ARTigoTabooGameViewTests(TestCase):

    def test_get(self):
        pass

    def test_post(self):
        pass


class TagATagGameViewTests(TestCase):

    def test_get(self):
        pass

    def test_post(self):
        pass


class CombinoGameViewTests(TestCase):

    def test_get(self):
        pass

    def test_post(self):
        pass
