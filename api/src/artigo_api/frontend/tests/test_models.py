from datetime import datetime

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
    def setUp(self):
        # set up object
        # tagging = Tagging.objects.create(tag="Tagging")
        self.tagging_user = "username"
        self.tagging_gameround = 1
        self.tagging_resource = 1
        self.tagging_tag = "Tagging to test"
        self.tagging_created = datetime.now()
        self.tagging_score = 0
        self.tagging_origin = ""
        self.tagging = Tagging(user=self.tagging_user,
                               gameround=self.tagging_gameround,
                               resource=self.tagging_resource,
                               tag=self.tagging_tag,
                               created=self.tagging_created,
                               score=self.tagging_score,
                               origin=self.tagging_origin)

    def test_tag_label(self):
        tagging = Tagging.objects.get(id=1)
        field_label = tagging._meta.get_field('tag').verbose_name()
        self.assertEqual(field_label, 'tag')

    def test_str(self):
        """Test for string representation"""
        tagging = Tagging()
        self.assertEqual(str(tagging), tagging.tag)


class TagTests(TestCase):
    def setUp(self):
        self.tag_name = "name of the tag"
        self.tag_language = "language of tag"
        self.tag = Tag(name=self.tag_name,
                       language=self.tag_language)

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


class CombinationTests(TestCase):
    def setUp(self):
        self.combination_user = "name of user"
        self.combination_gameround = 1
        self.combination_resource = "reshashid"
        self.combination_tag_id = 2
        self.combination_created = datetime.now()
        self.combination_score = 0
        self.combination = Combination(user=self.combination_user,
                                       gameround=self.combination_gameround,
                                       resource=self.combination_resource,
                                       tag_id=self.combination_tag_id,
                                       created=self.combination_created,
                                       score=self.combination_score)


class GamesessionTests(TestCase):
    def setUp(self):
        self.gamesession_user = "username"
        self.gamesession_gametype = "imageLabeler"
        self.gamesession_created = datetime.now()
        self.gamesession = Gamesession(user=self.gamesession_user,
                                       gametype=self.gamesession_gametype,
                                       created=self.gamesession_created)


class GameroundTests(TestCase):
    def setUp(self):
        self.gameround_user = "username"
        self.gameround_gamesession = 1
        self.gameround_created = datetime.now()
        self.gameround_score = 0
        self.gameround = Gameround(user=self.gameround_user,
                                   gamesession=self.gameround_gamesession,
                                   created=self.gameround_created,
                                   score=self.gameround_score)


class GametypeTests(TestCase):
    def setUp(self):
        self.gametype_name = "NewGame"
        self.gametype_rounds = 5
        self.gametype_rounds_duration = 60
        self.gametype_enabled = True
        self.gameround = Gameround(name=self.gametype_name,
                                   rounds=self.gametype_rounds,
                                   rounds_duration=self.gametype_rounds_duration,
                                   enabled=self.gametype_enabled)

    def test_name_size(self):
        gametype = Gametype.objects.get(name="Gametype")
        max_length = gametype._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        gametype = Gametype()
        self.assertEqual(str(gametype), gametype.name)


class ResourceTests(TestCase):
    def setUp(self):
        self.resource_id = 1
        self.resource_hash_id = "hashid"
        self.resource_crators = "creator"
        self.resource_titles = "titles"
        self.resource_created_start = datetime.now()
        self.resource_created_end = datetime.now()
        self.resource_location = "Location"
        self.resource_institution_source = "source"
        self.resource_institution = "institution"
        self.resource_origin = ""
        self.resouce_enabled = True
        self.resource_media_type = "picture"
        self.resource = Resource(id=self.resource_id,
                                 hash_id=self.resource_hash_id,
                                 creators=self.resource_crators,
                                 titles=self.resource_titles,
                                 created_start=self.resource_created_start,
                                 created_end=self.resource_created_end,
                                 location=self.resource_location,
                                 institution_source=self.resource_institution_source,
                                 institution=self.resource_institution,
                                 origin=self.resource_origin,
                                 enabled=self.resouce_enabled,
                                 media_type=self.resource_media_type)

    def test_str(self):
        """Test for string representation"""
        resource = Resource()
        self.assertEqual(str(resource), resource.hash_id)


class TitleTests(TestCase):
    def setUp(self):
        self.title_name = "Title"
        self.title_language = "some other language"
        self.title_technique = "title technique"
        self.title_style = "title style"
        self.title_movement = "title movement"
        self.title_locations = "title locations"
        self.title_webpage = "www.title.com"
        self.title = Title(name=self.title_name,
                           language=self.title_language,
                           technique=self.title_technique,
                           style=self.title_style,
                           movement=self.title_movement,
                           locations=self.title_locations,
                           web_page=self.title_webpage)

    def test_str(self):
        """Test for string representation"""
        title = Title()
        self.assertEqual(str(title), title.name)


class CreatorTests(TestCase):
    def setUp(self):
        self.creator_name = "Artist"
        self.creator_born = datetime.now()
        self.creator_died = datetime.now()
        self.creator_nationality = "some nationality"
        self.creator_locations = "some location"
        self.creator_techniques = "technique"
        self.creator_webpage = "www.creator.com"
        self.creator = Creator(name=self.creator_name,
                               born=self.creator_born,
                               died=self.creator_died,
                               nationality=self.creator_nationality,
                               locations=self.creator_locations,
                               techniques=self.creator_techniques,
                               web_page=self.creator_webpage)

    def test_str(self):
        """Test for string representation"""
        creator = Creator()
        self.assertEqual(str(creator), creator.name)


class ArtStyleTests(TestCase):
    def setUp(self):
        self.artstyle_name = "style"
        self.artstyle_language = "some language"
        self.artstyle = ArtStyle(name=self.artstyle_name,
                                 language=self.artstyle_language)

    def test_str(self):
        """Test for string representation"""
        style = ArtStyle()
        self.assertEqual(str(style), style.name)


class ArtMovementTests(TestCase):
    def setUp(self):
        self.artmovement_name = "style"
        self.artmovement_language = "some language"
        self.artmovement = ArtMovement(name=self.artmovement_name,
                                       language=self.artmovement_language)

    def test_str(self):
        """Test for string representation"""
        movement = ArtMovement()
        self.assertEqual(str(movement), movement.name)


class ArtTechniqueTests(TestCase):
    def setUp(self):
        self.arttechnique_name = "technique"
        self.arttechnique_language = "some language"
        self.arttechnique = ArtTechnique(name=self.arttechnique_name,
                                         language=self.arttechnique_language)

    def test_str(self):
        """Test for string representation"""
        technique = ArtTechnique()
        self.assertEqual(str(technique), technique.name)


class WebPageTests(TestCase):
    def setUp(self):
        self.webpage_url = "some url"
        self.webpage_language = "language of wp"
        self.webpage = WebPage(url=self.webpage_url,
                               language=self.webpage_language)


class LocationTests(TestCase):
    def setUp(self):
        self.location_name = "some location"
        self.location_country = "country"
        self.location = Location(name=self.location_name,
                                 country=self.location_country)

    def test_str(self):
        """Test for string representation"""
        location = Location()
        self.assertEqual(str(location), location.name)


class InstitutionTests(TestCase):
    def setUp(self):
        self.institution_name = "Institution"
        self.institution_url = "some Institution"
        self.institution_resource_url = "www.institution.com"
        self.institution = Institution(name=self.institution_name,
                                       institution_url=self.institution_url,
                                       resource_url=self.institution_resource_url)

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
