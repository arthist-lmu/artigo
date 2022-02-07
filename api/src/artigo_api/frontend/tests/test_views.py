import pytest
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

# from frontend.models import *
# from frontend.views import *


class GameTypeViewTests(APITestCase):
    # def setUp(self):
    #     """Define the test client and other test variables."""
    #     self.client = APIClient()
    #     self.gametype_data = {'': ''}
    #     self.response = self.client.post(
    #         'http://localhost:8000/artigo_api/gametype',
    #         self.gametype_data,
    #         format="json")

    def test_get_queryset(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Gametype.objects.all()))

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gametype')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Gametype.objects.all()))


class GamesessionViewTests(APITestCase):

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gamesession')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Gamesession.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/gamesession')
        data = {
            'id': 'New tag id',
            'user': 'New tag',
            'gametype': 'some language',
            'created': 'New tag',
        }
        response = self.client.post('http://localhost:8000/artigo_api/gamesession', data=data, format='json')
        self.assertEqual(response.status_code, 200)


class GameroundViewTests(APITestCase):

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gameround')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Gameround.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gameround')
        data = {
            'id': 'New tag id',
            'user': 'New tag',
            'gamesession': 'some language',
            'created': 'New tag',
            'score': 'some language',
        }
        response = self.client.post('http://localhost:8000/artigo_api/gameround', data=data, format='json')
        self.assertEqual(response.status_code, 200)


class TaggingViewTests(APITestCase):

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tagging')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Tagging.objects.all().order_by('?').first()))

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tagging')
        data = {
            'id': 'New tag id',
            'tag': 'New tag',
            'gameround': 'New gameround',
            'created': 'date',
            'score': 'points',
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

    def test_get(self):
        # tag = Tag()
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tag')
        self.assertEqual(response.Response, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Tag.objects.all().order_by('?').first()))
        # self.assertEqual(response.data['name'], tag.name)

    def test_post(self):
        # TODO: REWRITE TO FIT TAG
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tag')
        data = {
            'id': 'New tag id',
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
        self.artigo_game_data = {'resource': '',
                                 'gamesession': '',
                                 'gameround': ''}

        self.response = self.client.get('http://localhost:8000/artigo_api/artigo_game/',
                                        self.artigo_game_data,
                                        format="json")

    def test_api_can_create_game_data(self):
        """Test the api has resource retrieve capability."""
        self.client = APIClient()
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        self.assertEqual(response.status_code, 200)

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


# class ARTigoTabooGameViewTests(APITestCase):
#     def test_get(self):
#         response = self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')
#         self.assertEqual(response.status_code, 200)

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
