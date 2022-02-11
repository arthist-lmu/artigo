from datetime import datetime

import pytest
import pytz

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


class TagTests(TestCase):
    def setUp(self):
        self.tag_name = "name of the tag"
        self.tag_language = "language of tag"
        self.tag = Tag.objects.create(name=self.tag_name, language=self.tag_language)

    def test_name_label(self):
        tag = Tag.objects.get(name=self.tag_name)
        field_label = tag._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_tag_size(self):
        tag = Tag.objects.get(name=self.tag_name)
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.tag), self.tag.name)


class TaggingTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.resource = Resource.objects.create(id=1, hash_id="ba6abce620f33fb98ce7caf992476a6e", origin="")
        self.tag = Tag.objects.create(name="tag to test", language="en")

        self.tagging_user = self.user
        self.tagging_gameround = self.gameround
        self.tagging_resource = self.resource
        # self.tag = self.tag
        self.tagging_tag = self.tag
        self.tagging_created = datetime.now()
        self.tagging_score = 0
        self.tagging_origin = ""
        self.tagging = Tagging.objects.create(user=self.tagging_user,
                                              gameround=self.tagging_gameround,
                                              resource=self.tagging_resource,
                                              tag=self.tag,
                                              created=self.tagging_created,
                                              score=self.tagging_score,
                                              origin=self.tagging_origin)

    def test_tag_label(self):
        tagging = Tagging.objects.get(user=self.user)
        field_label = tagging._meta.get_field('tag').verbose_name
        self.assertEqual(field_label, 'tag')

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.tagging), self.tagging.tag.name)


class CombinationTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(user=self.user, gametype=self.gametype,
                                                      created=datetime.utcnow().replace(tzinfo=pytz.UTC))
        self.gameround = Gameround.objects.create(user=self.user, gamesession=self.gamesession,
                                                  created=datetime.utcnow().replace(tzinfo=pytz.UTC), score=0)
        self.resource = Resource.objects.create(id=1, hash_id="ba6abce620f33fb98ce7caf992476a6e", origin="")
        self.tag1 = Tag.objects.create(name="tag", language="en")
        self.tag2 = Tag.objects.create(name="second tag", language="en")

        self.combination_user = self.user
        self.combination_gameround = self.gameround
        self.combination_resource = self.resource

        # self.combination_tag_id = [self.tag1, self.tag2]
        self.combination_created = datetime.now()
        self.combination_score = 0
        self.combination = Combination.objects.create(user=self.combination_user,
                                                      gameround=self.combination_gameround,
                                                      resource=self.combination_resource,
                                                      created=self.combination_created,
                                                      score=self.combination_score)
        self.combination.tag_id.add(self.tag1)
        self.combination.tag_id.add(self.tag2)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.combination), self.combination.tag_id)


class GamesessionTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession_user = self.user
        self.gamesession_gametype = self.gametype
        self.gamesession_created = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.gamesession = Gamesession.objects.create(user=self.gamesession_user,
                                                      gametype=self.gamesession_gametype,
                                                      created=self.gamesession_created)

    # def test_create_gamesession(self):
    #     gamesession = Gamesession.objects.create(gametype=self.gametype)
    #     assert gamesession.gametype.name == "NewGame"


class GameroundTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="carina")
        self.gametype = Gametype.objects.create(name="NewGame", rounds=5, round_duration=60, enabled=True)
        self.gamesession = Gamesession.objects.create(id=1, user=self.user, gametype=self.gametype, created=datetime.now())
        self.gameround_user = self.user
        self.gameround_gamesession = self.gamesession
        self.gameround_created = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.gameround_score = 0
        self.gameround = Gameround.objects.create(user=self.gameround_user,
                                                  gamesession=self.gameround_gamesession,
                                                  created=self.gameround_created,
                                                  score=self.gameround_score)

    # def test_create_gameround(self):
    #     gameround = Gameround.objects.create(created=self.gameround_created)
    #     assert gameround.created == datetime.now()


class GametypeTests(TestCase):
    def setUp(self):
        self.gametype_name = "NewGame"
        self.gametype_rounds = 5
        self.gametype_rounds_duration = 60
        self.gametype_enabled = True
        self.gametype = Gametype.objects.create(name=self.gametype_name, rounds=self.gametype_rounds,
                                                round_duration=self.gametype_rounds_duration,
                                                enabled=self.gametype_enabled)

    def test_name_size(self):
        gametype = Gametype.objects.get(name="NewGame")
        max_length = gametype._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.gametype), self.gametype.name)

    def test_create_gametype(self):
        gametype = Gametype.objects.create(name=self.gametype_name)
        assert gametype.name == "NewGame"


class GamemodeTests(TestCase):
    def setUp(self):
        self.gamemode_name = "NewGameMode"
        self.gamemode_media_type = "text"
        self.gamemode_enabled = True
        self.gamemode = Gamemode.objects.create(name=self.gamemode_name, media_type=self.gamemode_media_type,
                                                enabled=self.gamemode_enabled)

    def test_name_size(self):
        gamemode = Gamemode.objects.get(name="NewGameMode")
        max_length = gamemode._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_media_type_size(self):
        gamemode = Gamemode.objects.get(media_type="text")
        max_length = gamemode._meta.get_field('media_type').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.gamemode), self.gamemode.name)

    def test_create_gamemode(self):
        gamemode = Gamemode.objects.create(name=self.gamemode_name)
        assert gamemode.name == "NewGameMode"


class ResourceTests(TestCase):
    def setUp(self):
        self.locations = Location.objects.create(name="location", country="country")
        self.technique = ArtTechnique.objects.create(name="technique", language="en")
        self.style = ArtStyle.objects.create(name="style", language="en")
        self.movement = ArtMovement.objects.create(name="movement", language="en")
        self.webpage = WebPage.objects.create(url="www.webpage.com", language="en")

        self.creators = Creator.objects.create(name="creator", born=datetime.utcnow().replace(tzinfo=pytz.UTC),
                                               died=datetime.utcnow().replace(tzinfo=pytz.UTC), nationality="de")
        self.creators.locations.add(self.locations)
        self.creators.techniques.add(self.technique)
        self.creators.web_page.add(self.webpage)

        self.titles = Title.objects.create(name="title", language="de", style=self.style, movement=self.movement)
        self.titles.locations.add(self.locations)
        self.titles.web_page.add(self.webpage)

        self.resource_id = 1
        self.resource_hash_id = "hashid"
        self.resource_crators = self.creators
        self.resource_titles = self.titles
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
        self.resource.titles.add(self.titles)
        self.resource.creators.add(self.creators)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.resource), self.resource.hash_id)


class TitleTests(TestCase):
    def setUp(self):
        self.locations = Location.objects.create(name="location", country="country")
        self.technique = ArtTechnique.objects.create(name="technique", language="en")
        self.style = ArtStyle.objects.create(name="style", language="en")
        self.movement = ArtMovement.objects.create(name="movement", language="en")
        self.webpage = WebPage.objects.create(url="www.webpage.com", language="en")

        self.title_name = "titlename"
        self.title_language = "en"
        self.title_technique = self.technique
        self.title_style = self.style
        self.title_movement = self.movement
        self.title_locations = self.locations
        self.title_webpage = self.webpage
        self.title = Title.objects.create(name=self.title_name,
                                          technique=self.title_technique,
                                          style=self.title_style,
                                          movement=self.title_movement)
        self.title.locations.add(self.locations)
        self.title.web_page.add(self.webpage)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.title), self.title.name)

    def test_title_size(self):
        title = Title.objects.get(name="titlename")
        max_length = title._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_create_title(self):
        title = Title.objects.create(name=self.title_name)
        assert title.name == "titlename"


class CreatorTests(TestCase):
    def setUp(self):
        self.locations = Location.objects.create(name="location", country="country")
        self.technique = ArtTechnique.objects.create(name="technique", language="en")
        self.webpage = WebPage.objects.create(url="www.webpage.com", language="en")

        self.creator_name = "Artist"
        self.creator_born = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.creator_died = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.creator_nationality = "some nationality"

        self.creator = Creator.objects.create(name=self.creator_name,
                                              born=self.creator_born,
                                              died=self.creator_died,
                                              nationality=self.creator_nationality)
        self.creator.locations.add(self.locations)
        self.creator.techniques.add(self.technique)
        self.creator.web_page.add(self.webpage)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.creator), self.creator.name)

    def test_creator_size(self):
        creator = Creator.objects.get(name=self.creator_name)
        max_length = creator._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_create_creator(self):
        creator = Creator.objects.create(name=self.creator_name)
        assert creator.name == "Artist"


class ArtStyleTests(TestCase):
    def setUp(self):
        self.artstyle_name = "style"
        self.artstyle_language = "some language"
        self.artstyle = ArtStyle.objects.create(name=self.artstyle_name, language=self.artstyle_language)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.artstyle), self.artstyle.name)

    def test_style_size(self):
        artstyle = ArtStyle.objects.get(name=self.artstyle_name)
        max_length = artstyle._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_create_style(self):
        artstyle = ArtStyle.objects.create(name=self.artstyle_name)
        assert artstyle.name == "style"


class ArtMovementTests(TestCase):
    def setUp(self):
        self.artmovement_name = "movement"
        self.artmovement_language = "some language"
        self.artmovement = ArtMovement.objects.create(name=self.artmovement_name, language=self.artmovement_language)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.artmovement), self.artmovement.name)

    def test_movement_size(self):
        artmovement = ArtMovement.objects.get(name=self.artmovement_name)
        max_length = artmovement._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_create_movement(self):
        artmovement = ArtMovement.objects.create(name=self.artmovement_name)
        assert artmovement.name == "movement"


class ArtTechniqueTests(TestCase):
    def setUp(self):
        self.arttechnique_name = "technique"
        self.arttechnique_language = "some language"
        self.arttechnique = ArtTechnique.objects.create(name=self.arttechnique_name,
                                                        language=self.arttechnique_language)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.arttechnique), self.arttechnique.name)

    def test_technique_size(self):
        arttechnique = ArtTechnique.objects.get(name=self.arttechnique_name)
        max_length = arttechnique._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_create_technique(self):
        arttechnique = ArtTechnique.objects.create(name=self.arttechnique_name)
        assert arttechnique.name == "technique"


class WebPageTests(TestCase):
    def setUp(self):
        self.webpage_url = "www.website.com"
        self.webpage_language = "language"
        self.webpage = WebPage.objects.create(url=self.webpage_url, language=self.webpage_language)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.webpage), self.webpage.url)

    def test_create_webpage(self):
        webpage = WebPage.objects.create(url=self.webpage_url)
        assert webpage.url == "www.website.com"


class LocationTests(TestCase):
    def setUp(self):
        self.location_name = "some location"
        self.location_country = "country"
        self.location = Location.objects.create(name=self.location_name, country=self.location_country)

    def test_create_location(self):
        location = Location.objects.create(name="new location")
        assert location.name == "new location"

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.location), self.location.name)

    def test_location_size(self):
        location = Location.objects.get(name=self.location_name)
        max_length = location._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)


class InstitutionTests(TestCase):
    def setUp(self):
        self.institution_name = "Institution"
        self.institution_url = "some Institution"
        self.institution_resource_url = "www.institution.com"
        self.institution = Institution.objects.create(name=self.institution_name,
                                                      institution_url=self.institution_url,
                                                      resource_url=self.institution_resource_url)

    def test_create_institution(self):
        institution = Institution.objects.create(name="Institution")
        assert institution.name == "Institution"

    def test_size_institution(self):
        institution = Institution.objects.get(name=self.institution_name)
        max_length = institution._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_str(self):
        """Test for string representation"""
        self.assertEqual(str(self.institution), self.institution.name)

