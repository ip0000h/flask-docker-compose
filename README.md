docker-flask
============

[![Build Status](https://travis-ci.org/ip0000h/docker-flask.svg)](https://travis-ci.org/ip0000h/docker-flask)

## Application scheme

Including the followings:

- Flask application running on uwsgi with next extensions:
  - Flask-Admin
  - Flask-Bcrypt
  - Flask-DebugToolbar
  - Flask-Login
  - Flask-Migrate
  - Flask-Script
  - Flask-SQLAlchemy
  - Flask-Testing
  - Flask-WTF


- PostgreSQL database(application uses SQLAlchemy library)


- Nginx frontend server for production mode



## Pre-Build

- install docker [https://github.com/docker/docker](https://github.com/docker/docker)

- install docker-compose [https://docs.docker.com/compose/install](https://docs.docker.com/compose/install)



## Usage

### Build an image

- ```docker-compose build flaskapp```


### Start a cluster:

To start applications with development environment:

- ```docker-compose up -d```

To start applications with production environment(first copy configuration file and edit it)
- ```docker-compose run --rm flaskapp cp settings/prod.py.repl settings/prod.py```
- ```docker-compose --file docker-compose.prod.yml up -d```

To initialize, create migration and upgrade your database:

- ```docker-compose run --rm flaskapp bash -c "python manage.py db init && python manage.py db migrate && python manage.py db upgrade && python manage.py create_user -i"```


### Stop and destroy a cluster:

To stop applications with development environment:

- ```docker-compose stop && docker-compose rm -f```

To stop applications with production environment:

- ```docker-compose --file docker-compose.prod.yml stop && docker-compose --file docker-compose.prod.yml rm -f```


### Logs and troubleshooting:

- ```docker-compose logs```


### Running tests:

- ```docker-compose run --rm flaskapp python test.py```
