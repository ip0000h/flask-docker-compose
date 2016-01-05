# -*- coding: utf-8 -*-
from sqlalchemy import func
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr


db = SQLAlchemy()


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=func.now())
