#!/bin/bash

python3 -m artigo_search --mode server -v -c /config.json &
exec celery -A core worker -l INFO &
exec celery -A core beat -l INFO
