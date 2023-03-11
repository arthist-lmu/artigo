import logging

from django.db import models
from django.db.models import Count, UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from frontend.fields import NameField
from frontend.managers import CustomUserManager, ResourceManager

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, unique=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_uploader = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    @property
    def n_rois(self):
        return self.rois.count()

    @property
    def n_taggings(self):
        return self.taggings.count()

    @property
    def n_annotations(self):
        return self.n_rois + self.n_taggings

    @property
    def n_resources(self):
        resources = self.taggings.values('resource') \
            .annotate(count=Count('resource')) \
            .values_list('resource_id', flat=True)

        return len(set(resources))

    @property
    def n_collections(self):
        return self.collections.count()

    @property
    def n_gamesessions(self):
        return self.gamesessions.count()


class CollectionTitle(models.Model):
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=256, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'language'],
                name='name_language_unique',
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.language = self.language.lower()
        
        return super().save(*args, **kwargs)


class Collection(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='collections',
    )
    hash_id = models.CharField(max_length=256)
    titles = models.ManyToManyField(
        CollectionTitle,
        related_name='collections',
    )
    access = models.CharField(
        max_length=2,
        choices=[
            ('O', 'Open'),
            ('P', 'Pending'),
            ('R', 'Restricted'),
        ],
        default='R',
    )
    status = models.CharField(
        max_length=2,
        choices=[
            ('U', 'Uploading'),
            ('F', 'Finished'),
            ('E', 'Error'),
        ],
        default='U',
    )
    progress = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def n_resources(self):
        return self.resources.count()
    

class Source(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField(max_length=256)

    def __str__(self):
        return self.name


class Creator(models.Model):
    wikidata_id = models.CharField(max_length=256, blank=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    collection = models.ForeignKey(
        Collection,
        related_name='resources',
        on_delete=models.CASCADE,
        null=True,
    )
    wikidata_id = models.CharField(max_length=256, blank=True)
    hash_id = models.CharField(max_length=256)
    creators = models.ManyToManyField(Creator)
    titles = models.ManyToManyField(Title)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        null=True,
    )
    created_start = models.IntegerField(null=True)
    created_end = models.IntegerField(null=True)
    location = models.CharField(max_length=512, blank=True)
    institution = models.CharField(max_length=512, blank=True)
    origin = models.URLField(max_length=256, blank=True)
    enabled = models.BooleanField(default=True)

    objects = ResourceManager()

    def __str__(self):
        return str(self.id)

    @property
    def tags(self):
        tags = self.taggings.values('tag') \
            .annotate(count=Count('tag'))

        return tags.values(
            'tag_id',
            'tag__name',
            'tag__language',
            'count',
        )


class GeneralType(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class GameType(GeneralType):
    enabled = models.BooleanField(default=True)


class OpponentType(GeneralType):
    pass


class InputType(GeneralType):
    pass


class TabooType(GeneralType):
    pass


class SuggesterType(GeneralType):
    pass


class ScoreType(GeneralType):
    pass


class Gamesession(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='gamesessions',
        null=True,
    )
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    rounds = models.PositiveIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    round_duration = models.PositiveIntegerField(
        default=60,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(60 * 60),
        ],
    )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class Gameround(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='gamerounds',
        null=True,
    )
    gamesession = models.ForeignKey(Gamesession, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)
    opponent_type = models.ForeignKey(
        OpponentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    input_type = models.ForeignKey(
        InputType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    taboo_type = models.ForeignKey(
        TabooType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    suggester_types = models.ManyToManyField(SuggesterType)
    score_types = models.ManyToManyField(ScoreType)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)


class GameroundParameter(models.Model):
    gameround = models.ForeignKey(
        Gameround,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
    )
    plugin_type = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class Tag(models.Model):
    name = NameField(max_length=256)
    language = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.language = self.language.lower()
        
        return super().save(*args, **kwargs)


class GeneralTagging(models.Model):
    gameround = models.ForeignKey(
        Gameround,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class UserTagging(GeneralTagging):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='taggings',
        null=True,
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='taggings',
    )
    suggested = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)    


class OpponentTagging(GeneralTagging):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_after = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )


class InputTagging(GeneralTagging):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


class TabooTagging(GeneralTagging):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


class GeneralROI(models.Model):
    gameround = models.ForeignKey(
        Gameround,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    x = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )
    y = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )
    width = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )
    height = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class UserROI(GeneralROI):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='rois',
        null=True,
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='rois',
    )
    suggested = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)    


class OpponentROI(GeneralROI):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_after = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )


class InputROI(GeneralROI):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


class TabooROI(GeneralROI):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
