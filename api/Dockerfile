FROM python:3.8-alpine

RUN pip install pip --upgrade
RUN pip install poetry

COPY /api/pyproject.toml /api/poetry.lock /api/
RUN cd /api; poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN cd /api; pip install -r requirements.txt

COPY /api /api/

COPY /api/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
