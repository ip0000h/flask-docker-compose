# -*- coding: utf-8 -*-
from flask.ext.script import Manager, prompt, prompt_pass
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
    """Creates database migrations and upgrades it"""
    pass


@manager.command
def create_user(is_admin=False):
    """Creates an user in database"""
    username = prompt("Enter username")
    password1 = prompt_pass("Enter password")
    password2 = prompt_pass("Re-type password")
    if password1 == password2:
        new_user = User(username, password1)
        new_user.is_admin = is_admin
        db.session.add(new_user)
        db.session.commit()
        print('User {0} successfully created'.format(username))
    else:
        print("Error: Passwords don't match")


if __name__ == '__main__':
    manager.run()
