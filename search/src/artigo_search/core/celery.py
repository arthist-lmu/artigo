from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

app = Celery(
    'core',
    broker='redis://redisai:6379/3',
    backend='redis://redisai:6379/4',
)
app.autodiscover_tasks(['core'])

app.conf.beat_schedule = {
    'import_data': {
        'task': 'core.tasks.import_data',
        'schedule': crontab(day_of_week='1', hour=2, minute=30),
    },
    'delete_data': {
        'task': 'core.tasks.delete_data',
        'schedule': crontab(day_of_week='*', hour=2, minute=0),
    },
    'document_count': {
        'task': 'core.tasks.document_count',
        'schedule': timedelta(minutes=5),
    },
}
