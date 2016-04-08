#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

import coverage

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Server, prompt, prompt_bool, prompt_pass
from flask.ext.script.commands import Clean, ShowUrls

from app import create_app
from database import db
from users.models import User

app = create_app('manageapp', os.path.dirname(__file__))

manager = Manager(app)

manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=5000,
                           use_debugger=True))

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

@manager.shell
def make_shell_context():
    """ Create a python REPL with several default imports
        in the context of the app
    """
    return dict(app=app, db=db, User=User)


@manager.command
def create_db():
    """Create database migrations and upgrade it"""
    db.create_all()


@manager.command
def drop_db():
    """Drop all database"""
    if prompt_bool(
            "Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create_user(admin=False):
    """Creates an user in database"""
    username = prompt("Enter username")
    email = prompt("Enter email")
    password1 = prompt_pass("Enter password")
    password2 = prompt_pass("Re-type password")
    if password1 == password2:
        new_user = User(
            username=username,
            password=password1,
            email=email
        )
        new_user.is_admin = admin
        db.session.add(new_user)
        db.session.commit()
        print('User {0} successfully created'.format(username))
    else:
        print("Error: Passwords don't match")


@manager.command
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    else:
        return 1


if __name__ == '__main__':
    manager.run()
