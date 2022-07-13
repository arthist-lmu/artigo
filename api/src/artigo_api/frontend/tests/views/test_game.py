import uuid
import json
import pytest

from django.urls import is_valid_path
from frontend.models import UserTagging
from frontend.views import GameView
from .utils import Test


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='user',
        email='user@artigo.org',
        password=uuid.uuid4().hex,
    )


class TestGame(Test):
    name = 'game'
    view = GameView

    def test_path(self, path):
        assert is_valid_path(path)

    def test_not_authenticated(self, path):
        response = self.get_response(path)
        content = json.loads(response.content)

        assert response.status_code == 500
        assert content['detail'] == 'not_authenticated'

    def test_unknown_game_type(self, path, user):
        params = {'game_type': 'unknown_game_type'}
        response = self.get_response(path, params, user)
        content = json.loads(response.content)

        assert response.status_code == 500
        assert content['detail'] == 'unknown_game_type'

    def test_no_valid_gamesessions(self, path, user):
        response = self.get_response(path, {}, user)
        content = json.loads(response.content)

        assert response.status_code == 500
        assert content['detail'] == 'no_valid_gamesessions'

    def test_tagging(self, path, user):
        params = {'game_type': 'tagging'}
        response = self.get_response(path, params, user)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert content['type'] == 'ok'
        assert content.get('session_id')
        assert content['rounds'] == 5
        assert content['round_id'] == 1
