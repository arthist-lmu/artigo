from django.db import connection
from django.apps import apps
from django.core.management.color import no_style


def reset_cursor():
    configs = [apps.get_app_config(x) for x in ['frontend']]
    models = [list(config.get_models()) for config in configs]

    with connection.cursor() as cursor:
        for model in models:
            for sql in connection.ops.sequence_reset_sql(no_style(), model):
                cursor.execute(sql)
