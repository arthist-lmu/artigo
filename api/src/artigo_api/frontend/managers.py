import random

from django.db import models
from django.db.models import Count


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
