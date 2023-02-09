FROM python:3.10

ENV POETRY_VIRTUALENVS_CREATE=False

RUN pip install --no-cache-dir poetry

RUN addgroup --system --gid 1998 artigo \
    && adduser --system --ingroup artigo --uid 1999 artigo

COPY /search/pyproject.toml /search/poetry.lock /
RUN cd /search; poetry install

COPY --chown=artigo:artigo /search /search/
RUN pip install /search

COPY --chown=artigo:artigo /search/config.json /config.json

WORKDIR /api/src/artigo_search

COPY /search/docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
