FROM python:3.10

ENV PYTHONPATH=/api/src/
ENV POETRY_VIRTUALENVS_CREATE=False

RUN addgroup --system --gid 1998 artigo \
    && adduser --system --ingroup --uid 1999 artigo artigo

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

COPY --chown=artigo:artigo /api /api/
COPY --chown=artigo:artigo /search /search/
RUN pip install /search

COPY --chown=artigo:artigo plugin.config.json /config.json

WORKDIR /api/src/artigo_api

COPY /api/docker-entrypoint.sh /api/docker-entrypoint.sh
ENTRYPOINT ["/api/docker-entrypoint.sh"]
