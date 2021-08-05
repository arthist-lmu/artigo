FROM ubuntu:20.10

RUN DEBIAN_FRONTEND=noninteractive apt update --fix-missing -y
RUN DEBIAN_FRONTEND=noninteractive apt upgrade -y 
RUN DEBIAN_FRONTEND=noninteractive apt install python3-pip npm git -y
RUN DEBIAN_FRONTEND=noninteractive apt install libmariadbclient-dev -y

RUN pip install poetry

COPY poetry.lock /pyproject.toml /src /api/

RUN cd /api; poetry export -f requirements.txt --output requirements.txt
RUN cd /api; pip install -r requirements.txt
