# -*- coding: utf-8 -*-

"""Exchange models."""
# Import Stdlibs
import bcrypt

# Import local modules
from database import TimestampMixin, db


class Client(TimestampMixin, db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    phone = db.Column(db.String(64), nullable=True, unique=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    use2factor_auth = db.Column(db.Boolean(), nullable=False, default=False)
    send_sms_always = db.Column(db.Boolean(), nullable=False, default=False)
    last_date = db.Column(db.DateTime, nullable=True)
    confirmed_date = db.Column(db.DateTime, nullable=True)
    first_ip = db.Column(db.String(40), nullable=True)
    last_ip = db.Column(db.String(40), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)

    def __init__(self, email=None, password=None):
        if email is not None and password is not None:
            self.email = email
            self.set_password(password)
        else:
            if not (email is None and password is None):
                raise ValueError

    def __repr__(self):
        return "{0} {1} {2} {3}".format(self.id, self.email, self.is_active, self.is_admin)

    def check_password(self, given_password):
        return bcrypt.checkpw(given_password, self.password_hash)

    def set_password(self, new_password):
        self.password_hash = bcrypt.hashpw(new_password, bcrypt.gensalt())

    @property
    def is_authenticated(self):
        return True

    # The methods below are required by flask-login
    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # Serialize method for REST-API
    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'active': u'Да' if self.active else u'Нет',
            'use2factor_auth': u'Да' if self.use2factor_auth else u'Нет',
            'first_ip': self.first_ip,
            'last_ip': self.last_ip,
            'created_at': self.created_at,
            'confirmed_date': self.confirmed_date,
            'last_date': self.last_date
        }
