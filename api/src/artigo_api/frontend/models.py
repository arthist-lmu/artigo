from frontend.managers import CustomUserManager, ResourceManager

from django.db import models
from django.db.models import Count, Max
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', unique=True)
    username = models.CharField(max_length=256, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    date_joined = models.DateTimeField(editable=False, default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_uploader = models.BooleanField(default=False)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.username

    def __str__(self):
        return f'{self.email} ({self.username})' or ''


class Institution(models.Model):
    name = models.CharField(max_length=256)
    institution_url = models.URLField(max_length=256)
    resource_url = models.URLField(max_length=256, default='')

    objects = models.Manager()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ArtTechnique(models.Model):
    name = models.CharField(max_length=256)
    language = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ArtMovement(models.Model):
    name = models.CharField(max_length=256)
    language = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ArtStyle(models.Model):
    name = models.CharField(max_length=256)
    language = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=256)
    born = models.DateField(null=True)
    died = models.DateField(null=True)
    nationality = models.CharField(max_length=256, null=True)
    locations = models.ManyToManyField(Location)
    techniques = models.ManyToManyField(ArtTechnique)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=256, blank=True)
    technique = models.ForeignKey(ArtTechnique, on_delete=models.CASCADE, null=True)
    style = models.ForeignKey(ArtStyle, on_delete=models.CASCADE, null=True)
    movement = models.ForeignKey(ArtMovement, on_delete=models.CASCADE, null=True)
    locations = models.ManyToManyField(Location)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Resource(models.Model):
    # TODO: Find better solution for when new Resources are added!
    id = models.PositiveIntegerField(null=False, primary_key=True)
    hash_id = models.CharField(max_length=256)
    creators = models.ManyToManyField(Creator)
    titles = models.ManyToManyField(Title)
    created_start = models.DateField(null=True)
    created_end = models.DateField(null=True)
    location = models.CharField(max_length=512, null=True)
    # source_id = models.CharField(max_length=256)
    institution_source = models.CharField(max_length=512, blank=True)
    institution = models.CharField(max_length=512, blank=True)
    # TODO: Determine if URLField or FilePathField?!
    origin = models.URLField(max_length=256, null=True)
    enabled = models.BooleanField(default=True)
    media_type = models.CharField(max_length=256, default='picture')

    objects = models.Manager()

    def __str__(self):
        return self.hash_id or ''

    @property
    def tags(self):
        tags = self.taggings.values('tag').annotate(count=Count('tag'))

        return tags.values('tag_id', 'tag__name', 'tag__language', 'count')


class Gametype(models.Model):
    name = models.CharField(max_length=256)
    rounds = models.PositiveIntegerField(default=5)
    round_duration = models.PositiveIntegerField(default=60)
    enabled = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


# class Gamemode(models.Model):
#     name = models.CharField(max_length=256, default='text')
#     media_type = models.CharField(max_length=256)
#     enabled = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         pass


class Gamesession(models.Model):
    # gamemode = models.ForeignKey(Gamemode, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    gametype = models.ForeignKey(Gametype, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class Gameround(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    gamesession = models.ForeignKey(Gamesession, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)

    def create(self):
        pass

    @property
    def tags(self):
        tags = self.taggings.values('tag')

        return tags.values('tag_id', 'tag__name', 'tag__language', 'resource_id')


class Tag(models.Model):
    # TODO: see if name should be oneToManyField instead of charfield
    name = models.CharField(max_length=256)
    language = models.CharField(max_length=256)

    objects = models.Manager()

    def __str__(self):
        return self.name or ''


class Tagging(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    gameround = models.ForeignKey(Gameround, on_delete=models.CASCADE, related_name='taggings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='taggings')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)
    # media_type = models.ForeignKey(Gamemode, on_delete=models.CASCADE)
    origin = models.URLField(max_length=256, blank=True, default='')

    objects = models.Manager()

    # TODO: finish the create method in order to do the POST
    def create(self, tag):
        tagging = self.create(tag=tag)

    def __str__(self):
        return str(self.tag) or ''

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


# class WebPages(models.Model):
#     # TODO: find better solution! (see below as well)
#     about_creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
#     about_title = models.ForeignKey(Title, on_delete=models.CASCADE)
#     url = models.URLField(max_length=256)
#     language = models.CharField(max_length=256)
#
#     def __str__(self):
#         return self.about_creator
