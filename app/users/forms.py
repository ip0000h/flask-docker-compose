# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

from database import db
from models import User


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = db.session.query(User).filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('invalid password')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    username = TextField('username', validators=[Required()])
    email = TextField('email address', [Required(), Email()])
    password = PasswordField('password', validators=[Required()])
    confirm = PasswordField('repeat password', [
        Required(),
        EqualTo('password', message='passwords must match')
        ])
    recaptcha = RecaptchaField()
