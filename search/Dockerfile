FROM python:3.10

RUN pip install --no-cache-dir poetry
COPY /search/pyproject.toml /search/poetry.lock /
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt

COPY /search/ /search/
RUN pip install /search

COPY /search/config.json /config.json

COPY /search/docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
