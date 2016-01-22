from flask.ext.mail import Message


@celery.task(bind=True, name='test', max_retries=None)
def test(self):
    with app.app_context():
        return 'ok!'


@celery.task(bind=True, name='send_email', max_retries=None)
def send_email(self, email, theme, message):
    with app.app_context():
        msg = Message(theme, recipients=[email])
        msg.body = message + u""" \n
        """
        return mail.send(msg)
