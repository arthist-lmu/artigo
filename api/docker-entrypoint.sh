#!/bin/bash

python3 manage.py runserver 0.0.0.0:8000 &
exec celery -A core worker -l INFO -n api@%h &
exec celery -A core beat -l INFO
