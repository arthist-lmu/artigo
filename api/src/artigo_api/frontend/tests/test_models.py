import uuid
import pytest

from frontend.models import *
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUser:
    def test_create_default(self):
        user = get_user_model().objects.create_user(
            username='user',
            email='user@artigo.org',
            password=uuid.uuid4().hex,
        )

        assert user.username == 'user'
        assert user.get_username() == 'user'
        assert user.email == 'user@artigo.org'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

        with pytest.raises(TypeError):
            user = get_user_model().objects.create_user(
                email='user@artigo.org',
                password=uuid.uuid4().hex,
            )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            username='user',
            email='user@artigo.org',
            password=uuid.uuid4().hex,
        )

        assert user.username == 'user'
        assert user.get_username() == 'user'
        assert user.email == 'user@artigo.org'
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser

        with pytest.raises(TypeError):
            user = get_user_model().objects.create_superuser(
                email='user@artigo.org',
                password=uuid.uuid4().hex,
            )


@pytest.mark.django_db
def test_resource_tags_property():
    tagging = UserTagging.objects.get(id=1)

    for value in tagging.resource.tags:
        assert value['count'] > 0
