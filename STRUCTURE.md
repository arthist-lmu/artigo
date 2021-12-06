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
The backend container starts on an Ubuntu base image and executes a Django server. The server runs a single application called `frontend`, which presents the APIs for ARTigo. Dependency management is done via [poetry](https://python-poetry.org/). It uses additional third-party packages aside from django-rest-framework:
* [dj-rest-auth](https://github.com/iMerica/dj-rest-auth) for authentication/account setup via API
* [allauth](https://github.com/pennersr/django-allauth) for social logins (Google, Facebook)
* [django-environ](https://github.com/joke2k/django-environ) for configuration using env-variables
by Django REST framework (which is also used by the backend).

## web
This container starts an Apache web server that uses the generated [Vue.js](https://vuejs.org/) files to act as a web client. For visual appeal it has the [vuetify](https://vuetifyjs.com/) UI-framework installed, in addition to [vue-router](https://router.vuejs.org/) for routing. It uses [Axios](https://axios-http.com/) to communicate with the backend. For performance reasons [webpack](https://webpack.js.org/) is used to bundle modules.


# Authentification
To enable SAML Auth with LMU-Services see [here](https://doku.lrz.de/pages/viewpage.action?pageId=56919067)