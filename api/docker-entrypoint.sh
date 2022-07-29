#!/bin/bash

python /api/artigo_api/manage.py runserver 0.0.0.0:8000 &
cd /api && exec celery -A artigo_api.core worker -l INFO -n api@%h &
cd /api && exec celery -A artigo_api.core beat -l INFO
