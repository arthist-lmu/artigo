import pytest

from django.test import TestCase
from rest_framework import response, status

from frontend.models import *
from frontend.serializers import *
from frontend.views import *


class GameViewControllerTests(TestCase):

    def test_test_get_random_object(self):
        pass

    def test_test_get_random_id(self):
        pass

    def test_get_gameround_matching_resource(self):
        pass

    def test_timer(self):
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
        # TODO: REWRITE TO FIT TAGGING
        data = {
            'id': 'New tag id',
            'tag': 'New tag',
            'gameround': 'New gameround',
            'created': 'date',
            'score': 'points',
            'resource': 'resource hash id',
        }
        self.assertEqual(Tagging.objects.count(), 0)
        # TODO: figure out what to replace list_url with in this case
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tagging.objects.count(), 1)
        tagging = Tagging.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(tagging, field_name), data[field_name])


class TagViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tag')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        # TODO: REWRITE TO FIT TAGGING
        data = {
            'id': 'New tag id',
            'name': 'New tag',
            'language': 'New gameround',
        }
        self.assertEqual(Tag.objects.count(), 0)
        # TODO: figure out what to replace list_url with in this case
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        tag = Tag.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(tag, field_name), data[field_name])


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
