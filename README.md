# ARTigo

<p float="left">
	<img src="images/home.png" width="250" hspace="10" />
	<img src="images/search-modal.png" width="250" hspace="10" /> 
	<img src="images/search.jpg" width="250" hspace="10" />
</p>

<p float="left">
	<img src="images/game-config.png" width="250" hspace="10" />
	<img src="images/game.png" width="250" hspace="10" /> 
	<img src="images/game-result.png" width="250" hspace="10" />
</p>


[![Web Testing](https://github.com/arthist-lmu/artigo/actions/workflows/build-web-testing.yml/badge.svg)](https://github.com/arthist-lmu/artigo/actions/workflows/build-web-testing.yml)
[![Api Testing](https://github.com/arthist-lmu/artigo/actions/workflows/build-api-testing.yml/badge.svg)](https://github.com/arthist-lmu/artigo/actions/workflows/build-api-testing.yml)
[![Search Testing](https://github.com/arthist-lmu/artigo/actions/workflows/build-search-testing.yml/badge.svg)](https://github.com/arthist-lmu/artigo/actions/workflows/build-search-testing.yml)

## Overview

Art history thrives on working with artworks and their digital reproductions. These are collected online in image catalogues, some of which contain several million objects. To search for images in such directories, descriptive texts are needed: a task you can help us with in a playful way—and at the same time learn a lot about art!

ARTigo is a collaborative platform and an example of open university research in which you participate as a player. All ARTigo games work like this: You are presented with an image. The goal is to describe this image within a certain time with keywords (*tags*) in such a way that as many points as possible are scored. After you have played a predefined number of rounds, the metadata for the images become visible. In this way, you not only generate art-historical knowledge, but also collect it. Every tag you enter is saved and improves the search for artworks—a win-win situation.

## Development setup

### Requirements
* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

### Configuration files
Copy the contents of `.env.example` to `.env` and adjust the settings.

### Setup process
1. To import data, `.csv` and `.jsonl` files should be stored in the `./dump` and corresponding `.jpg` files in the `./media` folder.

2. For the OpenSearch container to run properly, increase the virtual memory:
	```sh
	sudo sysctl -w vm.max_map_count=262144
	```

3. Create an unprivileged `artigo` user and group to own the files:
	```sh
	sudo addgroup --system --gid 1998 artigo && sudo adduser --system --uid 1999 --ingroup artigo artigo
	```

4. Build and start the container:
	```sh
	sudo docker-compose up --build
	```

5. Install `npm`:
	```sh
	sudo docker-compose exec web npm install
	```

6. Apply necessary Django operations and import fixtures:
	```sh
	sudo docker-compose exec api python3 manage.py migrate
	sudo docker-compose exec api python3 manage.py loaddata sites.json
	```

7. Import the data into `api` and `search`:
	```sh
	sudo docker-compose exec api python3 manage.py import_data
	sudo docker-compose exec search python3 -m artigo_search --mode client --task insert
	```


## Miscellaneous

### Code reloading
Hot reloading is enabled for `api`. To display changes of `web` (`http://localhost:8080/`), run:
```sh
sudo docker-compose exec web npm run build
```

Alternatively, use `serve` to enable a hot reloaded instance on `http://localhost:8081/`:
```sh
sudo docker-compose exec web npm run serve
```

### Schema updating
To re-generate the OpenAPI 3.0 schema file, use the following command:
```sh
sudo docker-compose exec api python3 manage.py spectacular --file schema.yml
```

### Formatting
Lint can be used to help with standardized formatting:
```sh
sudo docker-compose exec web npm run lint --fix
```

### Database schema migration
To generate database schema migration files, use the following command:
```sh
sudo docker-compose exec api python3 manage.py migrate
```

## Contributing

Please report issues, feature requests, and questions to the [GitHub issue tracker](https://github.com/arthist-lmu/artigo/issues). We have a [Contributor Code of Conduct](https://github.com/arthist-lmu/artigo/blob/master/CODE_OF_CONDUCT.md). By participating in ARTigo you agree to abide by its terms.
