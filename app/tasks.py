from flask.ext.mail import Message

from run_celery import make_celery

celeryapp = make_celery()


@celeryapp.task
def send_email(self, email, theme, message):
    msg = Message(theme, recipients=[email])
    msg.body = message + u"\n"
    return mail.send(msg)
