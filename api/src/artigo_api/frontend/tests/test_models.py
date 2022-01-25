import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase
from frontend.models import *


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
        # set up object
        tagging = Tagging.objects.create(tag="Tagging")
        assert tagging.user
        assert tagging.gameround
        assert tagging.resource
        assert tagging.tag == "Tagging"
        assert tagging.created
        assert tagging.score
        assert tagging.origin is None

    def test_tag_label(self):
        tagging = Tagging.objects.get(id=1)
        field_label = tagging._meta.get_field('tag').verbose_name()
        self.assertEqual(field_label, 'tag')

    def test_str(self):
        """Test for string representation"""
        tagging = Tagging()
        self.assertEqual(str(tagging), tagging.tag)


class TagTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Tag")
        assert tag.name == "Tag"
        assert tag.language == tag.language

    def test_name_label(self):
        tag = Tag.objects.get(id=1)
        field_label = tag._meta.get_field('name').verbose_name()
        self.assertEqual(field_label, 'name')

    def test_tag_size(self):
        tag = Tag.objects.get(id=1)
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        tag = Tag()
        self.assertEqual(str(tag), tag.name)


class GamesessionTests(TestCase):
    def test_create_session(self):
        # session = Gamesession.objects.create()
        # assert session
        pass


class GameroundTests(TestCase):
    def test_create_round(self):
        round = Gameround.objects.create(id=1)
        assert round.id == 1


class GametypeTests(TestCase):
    def test_create_type(self):
        gametype = Gametype.objects.create(name="Gametype")
        assert gametype.name == "Gametype"

    def test_name_size(self):
        gametype = Gametype.objects.get(name="Gametype")
        max_length = gametype._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        gametype = Gametype()
        self.assertEqual(str(gametype), gametype.name)


class ResourceTests(TestCase):
    def test_create_resource(self):
        pass

    def test_str(self):
        """Test for string representation"""
        resource = Resource()
        self.assertEqual(str(resource), resource.hash_id)


class TitleTests(TestCase):
    def test_create_title(self):
        pass

    def test_str(self):
        """Test for string representation"""
        title = Title()
        self.assertEqual(str(title), title.name)


class CreatorTests(TestCase):
    def test_create_creator(self):
        pass

    def test_str(self):
        """Test for string representation"""
        creator = Creator()
        self.assertEqual(str(creator), creator.name)


class ArtStyleTests(TestCase):
    def test_create_style(self):
        pass

    def test_str(self):
        """Test for string representation"""
        style = ArtStyle()
        self.assertEqual(str(style), style.name)


class ArtMovementTests(TestCase):
    def test_create_movement(self):
        pass

    def test_str(self):
        """Test for string representation"""
        movement = ArtMovement()
        self.assertEqual(str(movement), movement.name)


class ArtTechniqueTests(TestCase):
    def test_create_technique(self):
        pass

    def test_str(self):
        """Test for string representation"""
        technique = ArtTechnique()
        self.assertEqual(str(technique), technique.name)


class LocationTests(TestCase):
    def test_create_location(self):
        pass

    def test_str(self):
        """Test for string representation"""
        location = Location()
        self.assertEqual(str(location), location.name)


class InstitutionTests(TestCase):
    def test_create_institution(self):
        institution = Institution.objects.create(name="Institution")
        assert institution.name == "Institution"

    def test_size_institution(self):
        institution = Institution.objects.get(name="Institution")
        max_length = institution._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        institution = Institution()
        self.assertEqual(str(institution), institution.name)
