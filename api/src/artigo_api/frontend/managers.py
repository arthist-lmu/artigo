import random

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class ResourceManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('source')
        qs = qs.prefetch_related('creators', 'titles')

        return qs

    def random(self, seed=None):
        if seed:
            random.seed(seed)

        n_rows = self.all().count()
        row_id = random.randint(0, n_rows - 1)

        return self.all()[row_id]


class QuestionManager:
    pass