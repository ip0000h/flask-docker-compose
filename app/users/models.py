# -*- coding: utf-8 -*-

from flask.ext.bcrypt import check_password_hash, generate_password_hash
from sqlalchemy import orm, types, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(types.Integer, primary_key=True)
    username = Column(types.String(50), unique=True, nullable=False)
    email = Column(types.String(50), unique=True, nullable=True)
    is_active = Column(types.Boolean, nullable=False, default=True)
    is_admin = Column(types.Boolean, nullable=False, default=False)
    _password = Column('password', types.String(64), nullable=False)

    def __init__(self, username, password, email=None):
        self.username = username
        self.password = self.hash_password(password)
        self.email = email

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_admin(self):
        return self.is_admin

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = orm.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

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
