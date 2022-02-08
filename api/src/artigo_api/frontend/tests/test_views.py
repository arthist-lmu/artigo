from datetime import datetime

import pytest
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from frontend.models import *
from frontend.views import *
from frontend.serializers import *


class GameTypeViewTests(APITestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.gametype_data = {'name': 'imageLabeler'}
        self.response = self.client.post('http://localhost:8000/artigo_api/gametype',
                                         self.gametype_data, format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data), len(Gametype.objects.all().get(name=self.gametype_data)))


class GamesessionViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.gamesession_data = {'id': 1}
        self.response = self.client.get('http://localhost:8000/artigo_api/gamesession',
                                        self.gamesession_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gamesession')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(self.response.data), len(Gamesession.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/gamesession')
        data = {
            'id': 1,
            'user': CustomUser.objects.all().order_by('?').first(),
            'gametype': Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True),
            'created': datetime.now(),
        }
        response = self.client.post('http://localhost:8000/artigo_api/gamesession', data=data, format='json')
        self.assertEqual(response.status_code, 201)


class GameroundViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.gameround_data = {'id': 1}
        self.response = self.client.get('http://localhost:8000/artigo_api/gameround',
                                        self.gameround_data,
                                        format="json")
    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gameround')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(self.response.data), len(Gameround.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        # response = self.client.get('http://localhost:8000/artigo_api/gameround')
        data = {
            'id': 1,
            'user': None,
            'gamesession': Gamesession.objects.create(user=CustomUser.objects.create(username="carina"),
                                                      gametype=Gametype.objects.create(name="NewGame", rounds=5,
                                                                                       round_duration=60, enabled=True),
                                                      created=datetime.now()),
            'created': datetime.now(),
            'score': 0,
        }
        response = self.client.post('http://localhost:8000/artigo_api/gameround', data=data, format='json')
        self.assertEqual(response.status_code, 201)


class TaggingViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.tagging_data = {'id': 1}
        self.response = self.client.get('http://localhost:8000/artigo_api/tagging',
                                        self.tagging_data,
                                        format="json")
    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tagging')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data), len(Tagging.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tagging')
        data = {
            'id': 1,
            'tag': Tag.objects.create(name="new tagging", language="en"),
            'gameround': Gameround.objects.create(id=1,
                user=CustomUser.objects.create(username="carina"),
                                                  gamesession=Gamesession.objects.create(
                                                      user=CustomUser.objects.create(username="carina"),
                                                      gametype=Gametype.objects.create(name="NewGame", rounds=5,
                                                                                       round_duration=60, enabled=True),
                                                                                         created=datetime.now()),
                                                  created=datetime.now(),
                                                  score=0),
            'created': datetime.now(),
            'score': 0,
            'resource': 'resource hash id',
        }
        self.assertEqual(Tagging.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/tagging', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tagging.objects.count(), 1)
        tagging = Tagging.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(tagging, field_name), data[field_name])


class TagViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.tag_data = {'name': 'tag to test'}
        self.response = self.client.get('http://localhost:8000/artigo_api/tag',
                                        self.tag_data,
                                        format="json")
    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tag')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), len(Tag.objects.all().order_by('?').first()))
        # self.assertEqual(response.data['name'], tag.name)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tag')
        data = {
            'id': 1,
            'name': 'New tag',
            'language': 'some language',
        }
        self.assertEqual(Tag.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/tag', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        tag = Tag.objects.all().first()
        for field_name in data.keys():
            self.assertEqual(getattr(tag, field_name), data[field_name])


class GameResourceViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.resource_data = {'hash_id': '69ad9d0331e9316ca72881eeea0a4910'}
        self.response = self.client.get('http://localhost:8000/artigo_api/game_resource',
                                        self.resource_data,
                                        format="json")

    def test_api_can_retrieve_a_resource(self):
        """Test the api has resource retrieve capability."""
        self.client = APIClient()
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/game_resource')
        self.assertEqual(response.status_code, 200)


class ARTigoGameViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.resource = {'hash_id': '1404cc769fa538fab1b65b9cad201eca'}
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="imageLabeler", rounds=5, round_duration=60, enabled=True),
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype, created=datetime.now())
        self.gameround = Gameround.objects.create(user=self.user, gamesession=self.gamesession,
                                                  created=datetime.now(), score=0)
        self.artigo_game_data = {'gametype': self.gametype,
                                 'gamesession': self.gamesession,
                                 'gameround': self.gameround,
                                 'resource': self.resource}
        self.response = self.client.get('http://localhost:8000/artigo_api/artigo_game/',
                                        self.artigo_game_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        self.assertEqual(response.status_code, 200)

    def test_api_can_create_game_data(self):
        """Test the api has resource retrieve capability."""
        self.client = APIClient()
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        tag_data = {
            'id': 'New tag id',
            'name': 'New tag',
            'language': 'some language',
        }
        tagging_data = {
            'id': 'New tag id',
            'tag': tag_data,
            'gameround': 'New gameround',
            'created': 'date',
            'score': 'points',
            'resource': 'resource hash id',
        }

        response = self.client.post('http://localhost:8000/artigo_api/artigo_game/', data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ARTigoTabooGameViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_game/', format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')
        self.assertEqual(response.status_code, 200)

    # def test_post(self):
    #     response = self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')


# class TagATagGameViewTests(APITestCase):
#     def test_get(self):
#         response = self.client.get('http://localhost:8000/artigo_api/tagatag_game/')
#         self.assertEqual(response.status_code, 200)

    # def test_post(self):
    #     response = self.client.get('http://localhost:8000/artigo_api/tagatag_game/')


# class CombinoGameViewTests(APITestCase):
#     def test_get(self):
#         response = self.client.get('http://localhost:8000/artigo_api/combino_game/')
#         self.assertEqual(response.status_code, 200)

    # def test_post(self):
    #     response = self.client.get('http://localhost:8000/artigo_api/combino_game/')
