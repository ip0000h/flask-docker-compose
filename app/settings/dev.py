# -*- coding: utf-8 -*-
DEBUG = True
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

SQLALCHEMY_DATABASE_URI = 'postgresql://flask:flask@postgresql/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = True

CELERY_ENABLE_UTC = False
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TRACK_STARTED = True
CELERY_RESULT_PERSISTENT = True
CELERYD_POOL_RESTARTS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
