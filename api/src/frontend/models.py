import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(max_length=256)


class Creator(models.Model):
    name = models.CharField(max_length=256)


class Title(models.Model):
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=256, blank=True)


class ResourceManager(models.Manager):
    def random(self, seed=None):
        if seed:
            random.seed(seed)

        n_rows = self.all().count()
        row_id = random.randint(0, n_rows - 1)

        return self.all()[row_id]


class Resource(models.Model):
    hash_id = models.CharField(max_length=256)
    creators = models.ManyToManyField(Creator)
    titles = models.ManyToManyField(Title)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    created_start = models.DateField(null=True)
    created_end = models.DateField(null=True)
    location = models.CharField(max_length=512, blank=True)
    institution = models.CharField(max_length=512, blank=True)
    origin = models.URLField(max_length=256, blank=True)
    enabled = models.BooleanField(default=True)

    objects = ResourceManager()


class Gametype(models.Model):
    name = models.CharField(max_length=256)
    rounds = models.PositiveIntegerField(default=5)
    round_duration = models.PositiveIntegerField(default=60)
    enabled = models.BooleanField(default=True)


class Gamesession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gametype = models.ForeignKey(Gametype, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class Gameround(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gamesession = models.ForeignKey(Gamesession, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=256)
    language = models.CharField(max_length=256)


class Tagging(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gameround = models.ForeignKey(Gameround, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)
