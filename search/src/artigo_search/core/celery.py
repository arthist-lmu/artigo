import environ

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

env = environ.Env(
    REDIS_HOST=(str, 'redisai'),
    REDIS_PORT=(int, 6379),
)

app = Celery(
    'core',
    broker=f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/3',
    backend=f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}/4',
)
app.autodiscover_tasks(['core'])

app.conf.beat_schedule = {
    # 'import_data': {
    #     'task': 'core.tasks.import_data',
    #     'schedule': crontab(day_of_week='1', hour=2, minute=30),
    # },
    'document_count': {
        'task': 'core.tasks.document_count',
        'schedule': timedelta(minutes=5),
    },
}
