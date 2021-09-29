#Project structure
Artigo implements a Django backend (folder api) 
and a vue frontend (folder web). 

The project uses a docker-compose setup 
and deploys 5 containers:

* db
* redisai
* celery
* **api** (build with a dockerfile from an [ubuntu](https://ubuntu.com/) base image and with the contents of the api folder)
* **web** (build with a dockerfile from an [apache](https://httpd.apache.org/) base image and with the contents of the web folder)

##db
The [Postgres](https://www.postgresql.org/) database contains:
* Metadata for all collections (artists, dates, locations...)
* GWAP statistics (times played, tags...)
* User credential (usernames, emails, passwords)
##redisai
[Redis](https://redis.io/) is an in memory, key-value store database, that is used by celery for task management
##celery
[Celery](https://docs.celeryproject.org/en/stable/index.html) is a task queuing service, to allow for asynchronous task execution. For an example see this [tutorial](https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/).
##api
The backend container starts on an ubuntu base image and executes a django server. 
The server runs a single application called frontend, which presents the APIs for artigo.
It uses additional middleware:
* To enable [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
* [OauthToolkit](https://github.com/jazzband/django-oauth-toolkit) as [recommended](https://www.django-rest-framework.org/api-guide/authentication/#third-party-packages) 
by django-rest-framework (which is also used by the backend)
##web
This container starts an apache webserver, which in uses the generated vue.js files to act as a web client.
It also uses [axios](https://axios-http.com/) to communicate with the backend.
