# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import orm, types

from flask.ext.bcrypt import check_password_hash, generate_password_hash
from flask.ext.login import UserMixin


from database import db, TimestampMixin

class User(db.Model, TimestampMixin, UserMixin):
    """User model class"""

    __tablename__ = 'users'
    id = db.Column(types.Integer, primary_key=True)
    username = db.Column(types.String(50), unique=True, nullable=False)
    email = db.Column(types.String(50), unique=True, nullable=False)
    _password = db.Column('password', types.String(64), nullable=False)
    is_active = db.Column(types.Boolean, nullable=False, default=True)
    last_login = db.Column(types.DateTime(timezone=True),
                           onupdate=datetime.utcnow())

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def _get_password(self):
        return self._password

    def set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = orm.synonym('_password',
                           descriptor=property(_get_password,
                                               set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(types.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(types.and_, criteria)
        return cls.query.filter(q)
