import pytest

from django.test import TestCase
from rest_framework import response

from frontend.models import *
from frontend.serializers import *
from frontend.views import *


class GameViewControllerTests(TestCase):

    def test_generate_random_id(self):
        pass

    def test_pick_random_object(self):
        pass

    def test_get_random_object(self):
        pass

    def test_test_get_random_id(self):
        pass

    def test_get_resource(self):
        pass

    def test_get_gameround_matching_resource(self):
        pass

    def test_timer(self):
        pass

    def test_get_gamesession(self):
        pass

    def test_check_tagging_exists(self):
        pass

    def test_calculate_score(self):
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


class GamesessionViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/gamesession')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/gamesession')
        pass


class GameroundViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/gameround')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/gameround')
        pass


class TaggingViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tagging')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        pass


class TagViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tag')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        pass


class GameResourceViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/game_resource')
        self.assertEqual(response.Response, 200)


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
