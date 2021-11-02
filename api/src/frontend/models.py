from .managers import ResourceManager, QuestionManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=256)
    institution_url = models.URLField(max_length=256)
    resource_url = models.URLField(max_length=256)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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


class CombinedTagging(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gameround = models.ForeignKey(Gameround, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    first_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    second_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class Question(models.Model):
    question = models.CharField(max_length=256)
    tag = models.CharField(max_length=256)
    language = models.CharField(max_length=256)

    question = QuestionManager()


class ChosenOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gameround = models.ForeignKey(Gameround, on_delete=models.CASCADE)
    first_resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    second_resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    third_resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class WebPages(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    url = models.URLField(max_length=256)

    def __str__(self):
        return self.creator
