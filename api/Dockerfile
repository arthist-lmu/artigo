FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update --fix-missing -y
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install python3-pip npm libpq-dev -y

RUN pip install poetry
RUN pip install pytest pytest-cov

COPY poetry.lock /pyproject.toml /src /api/

RUN cd /api; poetry export -f requirements.txt --output requirements.txt
RUN cd /api; pip install -r requirements.txt
