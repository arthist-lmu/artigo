# Project structure
ARTigo implements a Django backend (folder `api`) and a Vue.js frontend (folder `web`). The project uses a `docker-compose` setup and deploys 5 containers:
* db
* redisai
* celery
* api (build with a dockerfile from an [Ubuntu](https://ubuntu.com/) base image, includes the contents of the `api` folder)
* web (build with a dockerfile from an [Apache](https://httpd.apache.org/) base image, includes the contents of the `web` folder)

## db
The [Postgres](https://www.postgresql.org/) database contains:
* Metadata of all resources (artists, dates, locations, etc.)
* GWAP statistics (times played, tags, taggings, etc.)
* User credentials (usernames, emails, passwords, etc.)

## redisai
[Redis](https://redis.io/) is an in memory, key-value store database, that is used by celery for task management.

## celery
[Celery](https://docs.celeryproject.org/en/stable/index.html) is a task queuing service, to allow for asynchronous task execution. For an example see this [tutorial](https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/).

## api
The backend container starts on an Ubuntu base image and executes a Django server. The server runs a single application called `frontend`, which presents the APIs for ARTigo. It uses additional middleware:
* to enable [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
* [OauthToolkit](https://github.com/jazzband/django-oauth-toolkit) as [recommended](https://www.django-rest-framework.org/api-guide/authentication/#third-party-packages) 
by Django REST framework (which is also used by the backend).

## web
This container starts an Apache webserver that uses the generated Vue.js files to act as a web client. It uses [Axios](https://axios-http.com/) to communicate with the backend.
