from celery import Celery
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
        'schedule': timedelta(hours=12),
    },
}
