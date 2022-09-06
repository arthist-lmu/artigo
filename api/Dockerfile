FROM python:3.9

RUN pip install --no-cache-dir poetry

COPY /api/pyproject.toml /api/poetry.lock /api/
COPY /search/pyproject.toml /search/poetry.lock /search/

RUN cd /api; poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN cd /api; pip install --no-cache-dir -r requirements.txt

RUN cd /search; poetry export -f requirements.txt --output requirements.txt  --without-hashes
RUN cd /search; pip install --no-cache-dir -r requirements.txt

COPY /search /search/
RUN pip install /search

COPY /api /api
COPY plugin.config.json /config.json
ENV PYTHONPATH=/api/src/
WORKDIR /api/src/artigo_api

COPY /api/docker-entrypoint.sh /api/docker-entrypoint.sh
ENTRYPOINT ["/api/docker-entrypoint.sh"]
