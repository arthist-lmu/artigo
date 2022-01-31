import pytest
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from frontend.models import *
from frontend.serializers import *
from frontend.views import *


class GameViewControllerTests(TestCase):

    def test_get_random_object(self):
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
        data = {
            'id': 'New tag id',
            'user': 'New tag',
            'gametype': 'some language',
            'created': 'New tag',
        }


class GameroundViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/gameround')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/gameround')
        data = {
            'id': 'New tag id',
            'user': 'New tag',
            'gamesession': 'some language',
            'created': 'New tag',
            'score': 'some language',
        }


class TaggingViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tagging')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/tagging')
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
        response = self.client.post('http://localhost:8000/artigo_api/tagging', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tagging.objects.count(), 1)
        tagging = Tagging.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(tagging, field_name), data[field_name])


class TagViewTests(TestCase):

    def test_get(self):
        tag = Tag()
        self.client.get('http://localhost:8000/artigo_api/tag')
        self.assertEqual(response.Response, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], tag.name)

    def test_post(self):
        # TODO: REWRITE TO FIT TAG
        self.client.get('http://localhost:8000/artigo_api/tag')
        data = {
            'id': 'New tag id',
            'name': 'New tag',
            'language': 'some language',
        }
        self.assertEqual(Tag.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/tag', data=data)
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
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        tagging_data = {
            'id': 'New tag id',
            'tag': 'New tag',
            'gameround': 'New gameround',
            'created': 'date',
            'score': 'points',
            'resource': 'resource hash id',
        }
        tag_data = {
            'id': 'New tag id',
            'name': 'New tag',
            'language': 'some language',
        }

        response = self.client.post('http://localhost:8000/artigo_api/artigo_game/', data=tagging_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ARTigoTabooGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')


class TagATagGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/tagatag_game/')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/tagatag_game/')


class CombinoGameViewTests(TestCase):

    def test_get(self):
        self.client.get('http://localhost:8000/artigo_api/combino_game/')
        self.assertEqual(response.Response, 200)

    def test_post(self):
        self.client.get('http://localhost:8000/artigo_api/combino_game/')
