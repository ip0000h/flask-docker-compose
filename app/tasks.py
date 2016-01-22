# -*- coding: utf-8 -*-

from flask.ext.mail import Message

from extensions import mail
from run_celery import make_celery


celeryapp = make_celery()


@celeryapp.task
def send_email(email, theme, message):
    msg = Message(theme, recipients=[email])
    msg.body = message + u"\n"
    return mail.send(msg)
