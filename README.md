# ARTigo


## Installation
At a later point there will be a docker container provided here.


## Development setup

### Requirements
* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [poetry](https://pypi.org/project/poetry/) (When building without docker)

### Setup process
Create the `poetry.lock` file if it does not exist:
```sh
cd api
poetry install --no-root
```

To ensure that the data is retained, these local folders must be filled with data for migration:
```sh
* /media
* /dump
```

The container can then be built and started:
```sh
sudo docker-compose up --build
```

Subsequently, install `npm`:
```sh
sudo docker-compose exec web npm install
```

And apply necessary Django operations:
```sh
sudo docker-compose exec api python3 manage.py migrate auth
sudo docker-compose exec api python3 manage.py migrate
```


## Miscellaneous

### Data import and export
To import data, `.csv` files must be stored in the `./dump` and corresponding `.jpg` files in the `./media` folder. The following command must be executed while the application is running:
```sh
sudo docker-compose exec api python3 manage.py import --format csv --input /dump
```

To export data, execute the following command:
```sh
sudo docker-compose exec api python3 manage.py export --format jsonl --output /dump
```

### Code reloading
Hot reloading is enabled for `api`. To display changes of `web`, run:
```sh
sudo docker-compose exec web npm run build
```

### Django commands
Create superuser:
```sh
sudo docker-compose exec api python3 manage.py createsuperuser
```

Make migrations:
```sh
sudo docker-compose exec api python3 manage.py makemigrations
sudo docker-compose exec api python3 manage.py migrate
```

### Run tests
To run tests for `api`, use one of the following commands:
```sh
sudo docker-compose exec api python3 manage.py test --verbosity 2
sudo docker-compose exec api pytest --verbose
```

Coverage reports are stored in the `./api/src/artigo_api/htmlcov` folder.


## Known issues

On some systems, the `api` container starts before `db`. To fix this, restart `api`:
```sh
sudo docker-compose restart api
```


## Contributing

Please report issues, feature requests, and questions to the [GitHub issue tracker](https://github.com/arthist-lmu/artigo/issues). We have a [Contributor Code of Conduct](https://github.com/arthist-lmu/artigo/blob/master/CODE_OF_CONDUCT.md). By participating in ARTigo you agree to abide by its terms.
