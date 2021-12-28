import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase
from frontend.models import *


@pytest.mark.django_db
def test_create_source():
    institution = Institution.objects.create(name="Institution")
    assert institution.name == "Institution"
    assert source.name == "Source"


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo", username='')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='testadmin', email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'testadmin')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', username='')


class TaggingTests(TestCase):
    def test_create_tagging(self):
        pass


class TagTests(TestCase):
    def test_create_tag(self):
        pass


class GamesessionTests(TestCase):
    def test_create_session(self):
        pass


class GameroundTests(TestCase):
    def test_create_round(self):
        pass


class GametypeTests(TestCase):
    def test_create_type(self):
        pass


class ResourceTests(TestCase):
    def test_create_resource(self):
        pass


class TitleTests(TestCase):
    def test_create_title(self):
        pass


class CreatorTests(TestCase):
    def test_create_creator(self):
        pass


class ArtStyleTests(TestCase):
    def test_create_style(self):
        pass


class ArtMovementTests(TestCase):
    def test_create_movement(self):
        pass


class ArtTechniqueTests(TestCase):
    def test_create_technique(self):
        pass


class LocationTests(TestCase):
    def test_create_location(self):
        pass


class InstitutionTests(TestCase):
    def test_create_institution(self):
        pass
