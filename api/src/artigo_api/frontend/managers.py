import random
import logging

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import BaseUserManager

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError('User must have an username.')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have `is_staff=True`.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have `is_superuser=True`.')

        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


class ResourceManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset() \
            .select_related('source') \
            .prefetch_related('creators', 'titles')

        return qs
