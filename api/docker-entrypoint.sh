#!/bin/bash

uwsgi \
--socket :8000 \
--wsgi-file core/wsgi.py \
--master \
--processes 1 \
--threads 1 &
exec celery -A core worker -l INFO -n api@%h &
exec celery -A core beat -l INFO
