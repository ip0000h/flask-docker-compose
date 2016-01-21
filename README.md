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
  - Flask-Profiler - [https://github.com/muatik/flask-profiler](https://github.com/muatik/flask-profiler)
  - Flask-Script - [https://github.com/smurfix/flask-script](https://github.com/smurfix/flask-script)
  - Flask-SQLAlchemy - [https://github.com/mitsuhiko/flask-sqlalchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
  - Flask-Testing - [https://github.com/jarus/flask-testing](https://github.com/jarus/flask-testing)
  - Flask-WTF - [https://github.com/lepture/flask-wtf](https://github.com/lepture/flask-wtf)


- [Celery](http://www.celeryproject.org/install/) application


- [Supervisor](http://supervisord.org/) for managing python applications


- [PostgreSQL](http://www.postgresql.org/) database


- [Nginx](http://nginx.org/) frontend server for production mode(for production only)


- [Redis](http://redis.io/) server


- [RabbitMQ](http://www.rabbitmq.com/) server(for production only)



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

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py create_db"```

To run ipython debug flaskapp shell:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py shell"```

To create admin user:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py create_user -i```


### Stop and destroy a cluster:

To stop applications with development environment:

- ```docker-compose stop && docker-compose rm -f```

To stop applications with production environment:

- ```docker-compose --file docker-compose.prod.yml stop && docker-compose --file docker-compose.prod.yml rm -f```


### Logs and troubleshooting:

To check standard logs:

- ```docker-compose logs```

Access the application containers shell:

- ```docker exec -it dockerflask_flaskapp_1 bash```


### Running tests:

- ```docker exec -it dockerflask_flaskapp_1 bash -c "python manage.py runtests"```



[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/ip0000h/docker-flask/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
