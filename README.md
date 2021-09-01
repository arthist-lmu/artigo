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
sudo docker-compose exec api python3 manage.py collectstatic
sudo docker-compose exec api python3 manage.py migrate auth
sudo docker-compose exec api python3 manage.py migrate
```

## Import data
To import data, `.csv` files must be stored in the `./dump` and corresponding `.jpg` files in the `./media` folder. The following command must be executed while the application is running:
```sh
sudo docker-compose exec api python3 manage.py import_csv /dump
```

## Update `web`
Hot reloading is enabled for `api`. To display changes of `web`, run:
```sh
sudo docker-compose exec web npm run build
```

## Django commands
Create superuser:
```sh
sudo docker-compose exec api python3 manage.py createsuperuser
```

Make migrations:
```sh
sudo docker-compose exec api python3 manage.py makemigrations
sudo docker-compose exec api python3 manage.py migrate
```