from datetime import datetime

import pytest
import json

import pytz
from django.urls import reverse, resolve
from rest_framework import response, status
from rest_framework.test import APITestCase, APIClient

from frontend.models import *
from frontend.views import *
from frontend.serializers import *


class GameTypeViewTests(APITestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.gametype_data = {'name': 'imageLabeler'}
        self.response = self.client.post(reverse('gametype'),
                                         self.gametype_data, format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get(reverse('gametype'))
        self.assertEqual(response.status_code, 200)


class GamesessionViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.user = CustomUser.objects.create(username="carina")
        self.created = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.gamesession_data = {'gametype': self.gametype}
        self.response = self.client.get(reverse('gamesession'),
                                        self.gamesession_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get(reverse('gamesession'))
        self.assertEqual(response.status_code, 200)


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
        response = self.client.post(reverse('tagging'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)


class CombinationViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="combino", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(id=1, user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.resource = Resource.objects.create(id=1, hash_id='resource hash id')
        self.tag_id = Tag.objects.create(name="new tagging", language="en")
        self.tag1 = Tag.objects.create(name="new tag", language="en")
        self.tag2 = Tag.objects.create(name="new tag two", language="en")
        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag1, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')

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
        response = self.client.post('http://localhost:8000/artigo_api/combination', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)


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
        response = self.client.post(reverse('tag'), data=data, format='json')
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

        self.response = self.client.get(reverse('Artigo game'),
                                        self.artigo_game_data,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get(reverse('Artigo game'))
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
        response = self.client.post(reverse('Artigo game'), data=tagging_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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
        response = self.client.post(reverse('ARTigo Taboo game'), data=tagging_data, format='json')
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
        response = self.client.post(reverse('Tag a Tag game'), data=tagging_data, format='json')
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
        self.tag1 = Tag.objects.create(name="new tag", language="en")
        self.tag2 = Tag.objects.create(name="new tag two", language="en")
        self.tagging = Tagging.objects.create(user=self.user, gameround=self.gameround, resource=self.resource,
                                              tag=self.tag1, created=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                              score=0, origin='')
        self.combination = {'tag_id': self.tag1}
        self.response = self.client.get(reverse('Combino game'),
                                        self.combination,
                                        format="json")

    def test_get(self):
        self.client = APIClient()
        response = self.client.get(reverse('Combino game'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client = APIClient()
        self.client.get('http://localhost:8000/artigo_api/combino_game/')

        tag1 = {'name': 'New tag', 'language': 'en'}
        tag2 = {'name': 'second tag', 'language': 'en'}

        combination_data = {
            'tag_id': [tag1, tag2],
            'gameround_id': 1,
            'resource_id': 1,
        }
        response = self.client.post(reverse('Combino game'), data=combination_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
