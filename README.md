docker-flask
============

[![Circle CI](https://circleci.com/gh/ip0000h/docker-flask.svg?style=svg)](https://circleci.com/gh/ip0000h/docker-flask)



## Application scheme

Including the followings:

- Docker and Docker-Compose for managing project

- [Flask](https://github.com/mitsuhiko/flask) application running on uwsgi with next extensions:
  - Flask-Admin - [https://github.com/flask-admin/flask-admin](https://github.com/flask-admin/flask-admin)
  - Flask-Bcrypt - [https://github.com/maxcountryman/flask-bcrypt](https://github.com/maxcountryman/flask-bcrypt)
  - Flask-DebugToolbar - [https://github.com/mgood/flask-debugtoolbar](https://github.com/mgood/flask-debugtoolbar)
  - Flask-Login - [https://github.com/maxcountryman/flask-login](https://github.com/maxcountryman/flask-login)
  - Flask-Mail - [https://github.com/mattupstate/flask-mail](https://github.com/mattupstate/flask-mail)
  - Flask-Migrate - [https://github.com/miguelgrinberg/Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
  - Flask-Script - [https://github.com/smurfix/flask-script](https://github.com/smurfix/flask-script)
  - Flask-SQLAlchemy - [https://github.com/mitsuhiko/flask-sqlalchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
  - Flask-Testing - [https://github.com/jarus/flask-testing](https://github.com/jarus/flask-testing)
  - Flask-WTF - [https://github.com/lepture/flask-wtf](https://github.com/lepture/flask-wtf)

- Celery application

- Supervisor for managing python applications

- PostgreSQL database

- Nginx frontend server for production mode(for production only)

- Redis server

- RabbitMQ server(for production only)



## Pre-Build

- install docker [https://github.com/docker/docker](https://github.com/docker/docker)

- install docker-compose [https://docs.docker.com/compose/install](https://docs.docker.com/compose/install)



## Usage

### Build an image:

- ```docker-compose build flaskapp```


### Start a cluster:

To start applications with development environment:

- ```docker-compose up -d```

To start applications with production environment(first copy configuration file and edit it)
- ```docker-compose run --rm flaskapp cp settings/prod.py.repl settings/prod.py```
- ```docker-compose --file docker-compose.prod.yml up -d```

To initialize, create migration and upgrade your database:

- ```docker-compose run --rm flaskapp bash -c "python manage.py db init && python manage.py db migrate && python manage.py db upgrade"```

To create admin user:

- ```docker-compose run --rm python manage.py create_user -i```


### Stop and destroy a cluster:

To stop applications with development environment:

- ```docker-compose stop && docker-compose rm -f```

To stop applications with production environment:

- ```docker-compose --file docker-compose.prod.yml stop && docker-compose --file docker-compose.prod.yml rm -f```


### Logs and troubleshooting:

To check standard logs:

- ```docker-compose logs```

Access the application containers shell(application containers name is dockerflask_flaskapp_1 by default):

- ```docker exec -it dockerflask_flaskapp_1 bash```


### Running tests:

- ```docker-compose run --rm flaskapp python test.py```
