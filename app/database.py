# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=func.now())
