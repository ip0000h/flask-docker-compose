from celery import Celery
from flask.ext.mail import Mail, Message

from app import app

mail = Mail()


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task(bind=True, name='send_email', max_retries=None)
def send_email(self, email, theme, message):
    with app.app_context():
        msg = Message(theme, recipients=[email])
        msg.body = message + u""" \n
        """
        mail.send(msg)
