from celery import Celery
from datetime import timedelta

app = Celery('core', broker='redis://localhost')
app.autodiscover_tasks(['core'])

app.conf.beat_schedule = {
  'import_jsonl': {
    'task': 'core.tasks.import_jsonl',
    'schedule': timedelta(hours=12),
  },
}