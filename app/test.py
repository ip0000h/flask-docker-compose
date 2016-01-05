# -*- coding: utf-8 -*-
import unittest
from flask.ext.testing import TestCase

from app import app, db
from models import User


class BaseTestCase(TestCase):
    """A base test case"""

    def create_app(self):
        app.config.from_object('settings.testing')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTestCase(BaseTestCase):
    """A user test case"""

    def test_user(self):
        user = User("admin", "ad@min.com", "admin")
        db.session.add(user)
        db.session.commit()
        assert user in db.session


class PageTestCase(BaseTestCase):
    """A pages test case"""

    def test_index_page(self):
        response = self.client.get("/")
        self.assert200(response)

    def test_secret_page(self):
        response = self.client.get("/secret")
        self.assert401(response)


if __name__ == '__main__':
    unittest.main()
