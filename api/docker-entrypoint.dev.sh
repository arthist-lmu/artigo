#!/bin/bash

uwsgi \
    --http :8000 \
    --wsgi-file core/wsgi.py \
    --master \
    --processes 1 \
    --buffer-size 32768 \
    --py-autoreload 3 \
    --uid 1999 \
    --threads 1 &
exec celery -A core worker -l INFO -n api@%h --uid 1999 &
exec celery -A core beat -l INFO
