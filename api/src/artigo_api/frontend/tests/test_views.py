import pytest

from django.test import TestCase
from rest_framework import response

from frontend.models import *
from frontend.serializers import *
from frontend.views import *


class GameViewControllerTests(TestCase):

    def test_calculate_score(self):
        pass

    def test_check_tag_exists(self):
        pass

    def test_generate_random_id(self):
        pass

    def test_pick_random_object(self):
        pass


class GameTypeViewTests(TestCase):

    def test_get_queryset(self):
        self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.Response, 200)
        self.assertEqual(len(response.responses), len(Gametype.objects.all()))

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.Response, 200)
        # self.assertEqual(len(response.responses), len(Gametype.objects.all()))


class ARTigoGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/artigo_game/')

    def test_post(self):
        pass


class ARTigoTabooGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')

    def test_post(self):
        pass


class TagATagGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tagatag_game/')

    def test_post(self):
        pass


class CombinoGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/combino_game/')

    def test_post(self):
        pass
