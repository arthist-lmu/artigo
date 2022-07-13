import json
import time
import pytest

from django.urls import is_valid_path
from frontend.views import SearchView
from .utils import Test


class TestSearch(Test):
    name = 'search'
    view = SearchView

    def test_path(self, path):
        assert is_valid_path(path)

    def test_string_query(self, path):
        params = {'params': {'query': 'adolph menzel'}}
        response = self.post_response(path, params)
        content = json.loads(response.content)

        while content.get('job_id'):
            time.sleep(0.5)

            params = {'params': content}
            response = self.post_response(path, params)
            content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('total')
        assert content.get('entries')
        assert len(content['entries']) > 0
