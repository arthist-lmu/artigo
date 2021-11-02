import random

from django.db import models


class ResourceManager(models.Manager):
    def random(self, seed=None):
        if seed:
            random.seed(seed)

        n_rows = self.all().count()
        row_id = random.randint(0, n_rows - 1)

        return self.all()[row_id]


class QuestionManager(models.Manager):
    # TODO: necessary methods here
    pass

