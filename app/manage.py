# -*- coding: utf-8 -*-

import os
import sys
from flask.ext.script import Manager, prompt, prompt_bool, prompt_pass
from flask.ext.migrate import Migrate, MigrateCommand

from app import app
from database import db
from models import User

db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


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
def runtests():
    """Run all tests"""
    pass


if __name__ == '__main__':
    manager.run()
