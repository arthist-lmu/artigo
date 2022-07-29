FROM python:3.9

RUN pip install poetry

COPY /api/pyproject.toml /api/poetry.lock /api/
RUN cd /api; poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN cd /api; pip install -r requirements.txt

COPY /api/src/ /api
COPY plugin.config.json /config.json

COPY /api/docker-entrypoint.sh /api/docker-entrypoint.sh
RUN chmod +x /api/docker-entrypoint.sh
ENTRYPOINT ["/api/docker-entrypoint.sh"]
