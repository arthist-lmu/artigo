FROM python:3.10

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt update && apt install -y build-essential python-dev
RUN pip install --no-cache-dir poetry

ARG VUE_APP_API
ENV VUE_APP_API=$VUE_APP_API

ARG VUE_APP_FRONTEND
ENV VUE_APP_FRONTEND=$VUE_APP_FRONTEND

COPY /api/pyproject.toml /api/poetry.lock /api/
RUN cd /api; poetry install

COPY /search/pyproject.toml /search/poetry.lock /search/
RUN cd /search; poetry install

COPY --chown=django:django /api /api
COPY --chown=django:django /search /search/
RUN pip install /search

COPY --chown=django:django plugin.config.json /config.json

ENV PYTHONPATH=/api/src/
WORKDIR /api/src/artigo_api

USER django

COPY /api/docker-entrypoint.sh /api/docker-entrypoint.sh
ENTRYPOINT ["/api/docker-entrypoint.sh"]
