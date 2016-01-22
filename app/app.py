# -*- coding: utf-8 -*-

# Import Flask app, modules and extensions
from flask import Flask
from flask import g, render_template
from flask.ext.admin import Admin
from flask.ext.login import current_user

# Import local modules
from admin.views import UserView, MyAdminIndexView
from database import db
from extensions import (
    debug_toolbar,
    login_manager
)
from models import User
from users.decorators import requires_login
from users.views import users as users_blueprint
from views import main_blueprint


__all__ = ['create_app']

DEFAULT_APP_NAME = 'flaskapp'


def create_app(config=None):
    """Flask app factory."""
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)

    configure_app(app, config)

    register_database(app)
    register_admin(app)
    register_extensions(app)
    register_blueprints(app)
    print(app.url_map)

    return app


def configure_app(app, config):
    """Configure application."""
    app.config.from_object('settings.base')
    if config is not None:
        if not app.config['TESTING']:
            app.config.from_envvar('FLASK_SETTINGS')
        else:
            app.config.from_object('settings.testing')


def register_admin(app):
    """Register admin application."""
    admin = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap3')
    admin.add_view(UserView(User, db.session))


def register_database(app):
    """Register database."""
    db.init_app(app)


def register_extensions(app):
    """Register all extensions."""
    login_manager.init_app(app)
    debug_toolbar.init_app(app)


def register_blueprints(app):
    """Register all blueprints."""
    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')
