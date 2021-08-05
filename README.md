# ARTigo

## Installation
Create the `poetry.lock` file if it does not exist:
```sh
cd api
poetry install --no-root
```

To ensure that the data is retained, local folders must be created and added to the `docker-compose.yml` file:
```sh
mkdir -p /data/artigo/web/media
mkdir -p /data/artigo/web/dump
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
sudo docker-compose exec api python manage.py collectstatic
sudo docker-compose exec api python manage.py migrate auth
sudo docker-compose exec api python manage.py migrate
```

## Import data
To import data, `.csv` files must be stored in the `/dump` and corresponding `.jpg` files in the `/media` folder. The following command must be executed while the application is running:
```sh
sudo docker-compose exec api python manage.py import_csv /dump
```

## Update `web`
Hot reloading is enabled for `api`. To display changes of `web`, run:
```sh
sudo docker-compose exec web npm run build
```

## Django commands
Create superuser:
```sh
sudo docker-compose exec api python manage.py createsuperuser
```

Make migrations:
```sh
sudo docker-compose exec api python manage.py makemigrations
sudo docker-compose exec api python manage.py migrate
```