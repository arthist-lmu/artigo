import pytest

from django.urls import reverse, is_valid_path
from rest_framework.test import force_authenticate, APIRequestFactory


@pytest.mark.django_db
class Test:
    factory = APIRequestFactory()

    @pytest.fixture
    def path(self):
        return reverse(self.name)

    def get_response(self, path, params={}, user=None):
        request = self.factory.get(path, params)

        if user is not None:
            force_authenticate(request, user=user)

        response = self.view.as_view()(request)
        response.render()

        return response

    def post_response(self, path, params={}, user=None):
        request = self.factory.post(path, params, format='json')

        if user is not None:
            force_authenticate(request, user=user)

        response = self.view.as_view()(request)
        response.render()

        return response
