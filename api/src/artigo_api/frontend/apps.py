from django.apps import AppConfig
from django.core.cache import cache


class FrontendConfig(AppConfig):
    name = 'frontend'

    def ready(self):
        from .tasks import renew_cache

        renew_cache(renew=False)
