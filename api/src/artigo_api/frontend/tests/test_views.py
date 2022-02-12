from datetime import datetime

import pytest
import json

import pytz
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
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.user = CustomUser.objects.create(username="carina")
        self.created = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.gamesession_data = {'gametype': self.gametype}
        self.response = self.client.get('http://localhost:8000/artigo_api/gamesession',
                                        self.gamesession_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gamesession')
        self.assertEqual(response.status_code, 200)
# TODO: Maybe test gamesession create
    # def test_post(self):
    #     self.client = APIClient()
    #     self.client.get('http://localhost:8000/artigo_api/gamesession')
    #     user = {'user': self.user.id}
    #     gametype = {"gametype": self.gametype.id}
    #     data = {
    #         'user': user,
    #         'gametype': gametype,
    #         'created': datetime.utcnow().replace(tzinfo=pytz.UTC),
    #     }
    #     response = self.client.post('http://localhost:8000/artigo_api/gamesession', data=data, format='json')
    #     self.assertEqual(response.status_code, 201)


class GameroundViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround_data = {'gamesession': self.gamesession}
        self.response = self.client.get('http://localhost:8000/artigo_api/gameround',
                                        self.gameround_data,
                                        format="json")
    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/gameround')
        self.assertEqual(response.status_code, 200)

    # TODO: Maybe test gameround create

    # def test_post(self):
    #     self.client = APIClient()
    #     self.client.get('http://localhost:8000/artigo_api/gameround')
    #     user = {'username': self.user.id}
    #     gamesession = {"gamesession": self.gamesession.id}
    #     data = {
    #         'user': user,
    #         'gamesession': gamesession,
    #         'created': datetime.utcnow().replace(tzinfo=pytz.UTC),
    #         'score': 0,
    #     }
    #     self.assertEqual(Gameround.objects.count(), 0)
    #     response = self.client.post('http://localhost:8000/artigo_api/gameround', data=data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Gameround.objects.count(), 1)
    #     gameround = Gameround.objects.all().first()
    #     for field_name in data.keys():
    #         self.assertEqual(getattr(gameround, field_name), data[field_name])


class TaggingViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.tag = Tag.objects.create(name="new tagging", language="en")
        self.resource = Resource.objects.create(id=1, hash_id='resource hash id')
        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')
        self.tagging = {'tag': self.tag}
        self.response = self.client.get('http://localhost:8000/artigo_api/tagging',
                                        self.tagging,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tagging')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tagging')
        tag = {'name': 'New tag', 'language': 'en'}
        data = {
            'tag': tag,
            'gameround_id': 1,
            'resource_id': 1,
        }
        # self.assertEqual(Tagging.objects.count(), 0)
        response = self.client.post(reverse('tagging'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        # self.assertEqual(Tagging.objects.count(), 1)
        # tagging = Tagging.objects.all().first()
        # for field_name in data.keys():
            # self.assertEqual(getattr(tagging, field_name), data[field_name])


class CombinationViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="combino", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype, created=datetime.now())
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.tag_id = Tag.objects.create(name="new tagging", language="en")
        self.resource = Resource.objects.create(id=1, hash_id='resource hash id')

        self.combination = {'tag': self.tag_id}
        self.response = self.client.get('http://localhost:8000/artigo_api/combination',
                                        self.combination,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/combination')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/combination')
        tag1 = {'name': 'New tag', 'language': 'en'}
        tag2 = {'name': 'secondtag', 'language': 'en'}
        data = {
            'tag_id': [tag1, tag2],
            'gameround_id': 1,
            'resource_id': 1,
        }
        # self.assertEqual(Combination.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/combination', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        # self.assertEqual(Combination.objects.count(), 1)
        # tagging = Combination.objects.all().first()
        # for field_name in data.keys():
            # self.assertEqual(getattr(tagging, field_name), data[field_name])


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

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tag')
        data = {
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
        self.resource_id = 1
        self.resource_hash_id = "hashid"
        self.resource_created_start = datetime.now()
        self.resource_created_end = datetime.now()
        self.resource_location = "Location"
        self.resource_institution_source = "source"
        self.resource_institution = "institution"
        self.resource_origin = ""
        self.resouce_enabled = True
        self.resource_media_type = "picture"
        self.resource = Resource.objects.create(id=self.resource_id,
                                                hash_id=self.resource_hash_id,
                                                created_end=self.resource_created_end,
                                                location=self.resource_location,
                                                institution_source=self.resource_institution_source,
                                                institution=self.resource_institution,
                                                origin=self.resource_origin,
                                                enabled=self.resouce_enabled,
                                                media_type=self.resource_media_type)
        self.resource_data = {'resource': self.resource.id}
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
        self.resource = Resource.objects.create(id=1, hash_id='1404cc769fa538fab1b65b9cad201eca')
        self.user = CustomUser.objects.create(id=1, username="carina")
        self.gametype = Gametype.objects.create(id=1, name="imageLabeler", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.tag = Tag.objects.create(name="new tag", language="en")

        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')

        self.artigo_game_data = {'resource': self.resource,
                                 'gameround': self.gameround,
                                 'gamesession': self.gamesession}

        self.response = self.client.get('http://localhost:8000/artigo_api/artigo_game/',
                                        self.artigo_game_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/artigo_game/')
        tag_data = {
            'name': 'New tag',
            'language': 'some language',
        }

        tagging_data = {
            'tag': tag_data,
            'gameround_id': 1,
            'resource_id': 1,
        }
        # self.assertEqual(Tagging.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/artigo_game/', data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Tagging.objects.count(), 1)
        # tagging = Tagging.objects.all().first()
        # for field_name in tagging_data.keys():
            # self.assertEqual(getattr(tagging, field_name), tagging_data[field_name])


class ARTigoTabooGameViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(id=1, username="carina")
        self.resource = Resource.objects.create(id=1, hash_id='1404cc769fa538fab1b65b9cad201eca')
        self.gametype = Gametype.objects.create(id=1, name="imageLabeler_Taboo", rounds=5,
                                                round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.tag = Tag.objects.create(name="new tag", language="en")
        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')
        self.response = self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/', format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/artigo_taboo_game/')
        tag_data = {
            'name': 'New tag',
            'language': 'some language',
        }

        tagging_data = {
            'tag': tag_data,
            'gameround_id': 1,
            'resource_id': 1,
        }
        response = self.client.post('http://localhost:8000/artigo_api/artigo_taboo__game/', data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TagATagGameViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(id=1, username="carina")
        self.resource = Resource.objects.create(id=1, hash_id='1404cc769fa538fab1b65b9cad201eca')
        self.gametype = Gametype.objects.create(id=1, name="imageAndTagLabeler", rounds=5,
                                                round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.tag = Tag.objects.create(name="new tag", language="en")
        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')

        self.response = self.client.get('http://localhost:8000/artigo_api/tagatag_game/', format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/tagatag_game/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/tagatag_game/')
        tag_data = {
            'name': 'New tag',
            'language': 'some language',
        }

        tagging_data = {
            'tag': tag_data,
            'gameround_id': 1,
            'resource_id': 1,
        }
        response = self.client.post('http://localhost:8000/artigo_api/tagatag_game/', data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CombinoGameViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(id=1, username="carina")
        self.resource = Resource.objects.create(id=1, hash_id='1404cc769fa538fab1b65b9cad201eca')
        self.gametype = Gametype.objects.create(id=1, name="Combino", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
#         self.combino_data = None
        self.response = self.client.get('http://localhost:8000/artigo_api/combino_game/', format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get('http://localhost:8000/artigo_api/combino_game/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/combino_game/')
        tag_data = {
            'name': 'New tag',
            'language': 'some language',
        }
        gameround = {'gameround': self.gameround.id}
        resource = {'resource': self.resource.id}
        tagging_data = {
            'tag': tag_data,
            'gameround_id': 1,
            'resource_id': 1,
        }
        self.assertEqual(Combination.objects.count(), 0)
        response = self.client.post('http://localhost:8000/artigo_api/combino_game/', data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Combination.objects.count(), 1)
        tagging = Combination.objects.all().first()
        for field_name in tagging_data.keys():
            self.assertEqual(getattr(tagging, field_name), tagging_data[field_name])
