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
    'import_jsonl': {
        'task': 'core.tasks.import_jsonl',
        'schedule': crontab(day_of_week='1', hour=2, minute=30),
    },
    'delete_jsonl': {
        'task': 'core.tasks.delete_jsonl',
        'schedule': crontab(day_of_week='*', hour=2, minute=0),
    },
    'log_count': {
        'task': 'core.tasks.log_count',
        'schedule': timedelta(minutes=5),
    },
}
