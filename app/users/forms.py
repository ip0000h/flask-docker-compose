# -*- coding: utf-8 -*-

"""Users forms."""
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length

from flask_wtf import Form, RecaptchaField

from database import db
from packages.users.models import Client


class EmailForm(Form):
    """Email form for reset password."""
    email = TextField(
        u'Email',
        validators=[DataRequired(), Email(), Length(max=128)]
    )


class PasswordForm(Form):
    """Password form."""
    password = PasswordField(
        u'Password',
        validators=[DataRequired()]
    )
    confirm = PasswordField(
        u'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message=u'Passwords must match.')
        ]
    )


class LoginForm(Form):
    """Login form."""
    email = TextField(
        u'Email',
        validators=[DataRequired(), Email(), Length(max=128)]
    )
    password = PasswordField(
        u'Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField(
        u'Remember me',
        default=False
    )

    def validate(self):
        """Validate the form."""
        rv = Form.validate(self)
        if not rv:
            return False

        user = db.session.query(Client).filter_by(
            email=self.email.data).first()

        if user is None:
            self.email.errors.append(u'Unknown email.')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append(u'Invalid password.')
            return False

        self.user = user

        return True


class SignUpForm(Form):
    """Registration user form."""
    email = TextField(
        u'Email',
        validators=[DataRequired(), Email(), Length(max=128)]
    )
    password = PasswordField(
        u'Password',
        validators=[DataRequired()]
    )
    confirm = PasswordField(
        u'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message=u'Passwords must match.')
        ]
    )
    recaptcha = RecaptchaField()

    def validate(self):
        """Validate the form."""
        rv = Form.validate(self)
        if not rv:
            return False

        user = db.session.query(Client).filter_by(
            email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered.')
            return False

        return True


class SettingsForm(Form):
    """User settings form."""
    email = TextField(
        u'Email',
        validators=[DataRequired(), Email(), Length(max=128)]
    )
    phone = TextField(
        u'Phone',
        validators=[Length(max=16)]
    )
    use2factor_auth = BooleanField(
        u'Use 2-factor auth',
        default=False
    )
    send_sms_always = BooleanField(
        u'Send sms always',
        default=False
    )
    password = PasswordField(
        u'Password',
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        u'New password'
    )
    confirm = PasswordField(
        u'Repeat new password',
        validators=[
            EqualTo('new_password', message=u'Passwords must match.')
        ]
    )
    recaptcha = RecaptchaField()

    def validate(self):
        """Validate the form."""
        rv = Form.validate(self)
        if not rv:
            return False

        return True
