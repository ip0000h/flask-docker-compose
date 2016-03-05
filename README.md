# flask-docker-compose

[![Circle CI](https://circleci.com/gh/ip0000h/flask-docker-compose.svg?style=svg)](https://circleci.com/gh/ip0000h/flask-docker-compose)

## About

Docker-Flask is about Flask project organization and running it in a
docker-compose containers.
Application has a basic user model with authentication(passwords hashing),
database migrations,
administration interface, celery asynchronous tasks, manage script,
debug toolbar, bootstrap starter templates.

## Application scheme

### Including the followings

-   Docker and Docker-Compose for managing project

-   [Flask](https://github.com/mitsuhiko/flask) application running on UWSGI
with next extensions:

    - [Flask-Admin](https://github.com/flask-admin/flask-admin)
    - [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt)
    - [Flask-DebugToolbar](https://github.com/mgood/flask-debugtoolbar)
    - [Flask-Login](https://github.com/maxcountryman/flask-login)
    - [Flask-Mail](https://github.com/mattupstate/flask-mail)
    - [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
    - [Flask-Script](https://github.com/smurfix/flask-script)
    - [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
    - [Flask-Testing](https://github.com/jarus/flask-testing)
    - [Flask-WTF](https://github.com/lepture/flask-wtf)


-   [Celery](http://www.celeryproject.org/install/) asynchronous tasks
application


-   [Supervisor](http://supervisord.org/) initialize system for managing python
applications


-   [PostgreSQL](http://www.postgresql.org/) object-relational database


-   [Nginx](http://nginx.org/) frontend web server for production
mode


-   [Redis](http://redis.io/) key-value storage server


-   [RabbitMQ](http://www.rabbitmq.com/) AMPQ server(for production only)


-   [Postfix](http://www.postfix.org/) SMTP mail server

## Pre-Build

-   install docker [https://github.com/docker/docker](https://github.com/docker/docker)
-   install docker-compose [https://docs.docker.com/compose/install](https://docs.docker.com/compose/install)

## Usage

### Build an image

-   ```docker-compose build flaskapp```

### Start a cluster

To start applications with development environment:

-   ```docker-compose up -d```

To start applications with production environment
(first copy configuration file and edit it)

-   ```cp app/settings/prod.py.repl app/settings/prod.py```
-   ```docker-compose --file docker-compose.prod.yml up -d```

To initialize, create migration and upgrade your database:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py create_db"```

To run ipython debug flaskapp shell:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py shell"```

To create admin user:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py create_user -a"```

### Migrations

To initialize migrations:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py db init"```

To create a migration:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py db migrate"```

To upgrade your database with migration:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py db upgrade"```

### Stop and destroy a cluster

- ```docker-compose stop && docker-compose rm -f```

### Logs and troubleshooting

To check standard logs:

- ```docker-compose logs```

Access the application containers shell:

- ```docker exec -it dockerflask_flaskapp_1 bash```

### Running tests

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py runtests"```
