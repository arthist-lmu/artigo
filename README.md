# ARTigo

## Installation
At a later point there will be a docker container provided here.

## Hosting Requirements

### Disk size
Postgres 1.6 GB after initial upload including all media files

### Memory
* 900 MB OpenSearch Idle
* 500 MB Django Idle
* 250 MB Postgres
* 400 MB other

→ 4 GB min for production use

## Development setup

### Requirements
* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [poetry](https://pypi.org/project/poetry/) (When building without docker and to create the `poetry.lock` file)

### Configuration Files
Copy the content of `.env.example` files to `.env` files in the same location and customize the settings.
For your local development setup configure app.config.js to use the local API endpoint.

### Setup process

To ensure that the data is retained, local folders must be filled with data for migration:
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
sudo docker-compose exec api python3 manage.py migrate
```

Import fixtures (i.e., initial data):
```sh
sudo docker-compose exec api python3 manage.py loaddata sites.json
```

Next: Follow the setup for the search container here ./search/README.md

## Miscellaneous

### Data import and export
When exporting from the legacy ARTigo instance use the conversion script on the dump folder first (Requires numpy and pandas).

```
python3 api/src/artigo_api/frontend/management/commands/convert_csv.py --input dump_input --output dump --image_input media_input --image_output media
```

To import data, `.csv` files should be stored in the `./dump` and corresponding `.jpg` files in the `./media` folder. The following command must be executed while the application is running:
```sh
sudo docker-compose exec api python3 manage.py import
```
While importing, please note that in comparison to earlier ARTigo, unique e-mails ARE enforced, and double accounts will not be created. 
Check user.csv for these errors. Importing the full data set can take a significant amount of time. (~26 min)

To export data, execute the following command:
```sh
sudo docker-compose exec api python3 manage.py export --format jsonl --output /dump
```

To connect directly to the database in the PostgreSQL container, use the following command:
```sh
sudo docker-compose exec -u postgres db psql -d artigo
```

### Code reloading
Hot reloading is enabled for `api`. 

To display changes of `web` (`http://localhost:8080/`), run:
```sh
sudo docker-compose exec web npm run build
```

Alternatively, use `serve` to enable a hot reloaded instance on `http://localhost:8081/`:
```sh
sudo docker-compose exec web npm run serve
```

### Formatting
Lint can be used to help with standardized formatting:
```sh
sudo docker-compose exec web npm run lint --fix
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


## Contributing

Please report issues, feature requests, and questions to the [GitHub issue tracker](https://github.com/arthist-lmu/artigo/issues). 
We have a [Contributor Code of Conduct](https://github.com/arthist-lmu/artigo/blob/master/CODE_OF_CONDUCT.md). 
By participating in ARTigo you agree to abide by its terms.
