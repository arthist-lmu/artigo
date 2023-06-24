#!/bin/bash

unset http_proxy; unset https_proxy; python -m artigo_search --mode server -v -c /config.json &
exec celery -A core worker -l INFO -n search@%h --uid 1999 &
exec celery -A core beat -l INFO
