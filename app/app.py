# -*- coding: utf-8 -*-

import os

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
    login_manager,
    mail
)
from users.models import User
from users.decorators import requires_login
from users.views import users as users_blueprint
from views import main_blueprint

# For import *
__all__ = ['create_app']

DEFAULT_APP_NAME = 'flaskapp'


def create_app(package_name, package_path, settings_override=None,
                register_security_blueprint=True):
    """Flask app factory."""
    app = Flask(package_name, instance_relative_config=False)

    configure_app(app, settings_override)

    configure_logging(app)

    register_database(app)
    register_error_handlers(app)
    register_admin(app)
    register_extensions(app)
    register_blueprints(app)

    return app


def configure_app(app, config=None):
    """Configure application."""
    app.config.from_object('settings.base')
    if not app.config['TESTING']:
        app.config.from_envvar('FLASK_SETTINGS')
    else:
        app.config.from_object('settings.testing')


def register_admin(app):
    """Register admin application."""
    admin = Admin(
        app,
        index_view=MyAdminIndexView(),
        template_mode='bootstrap3'
    )
    admin.add_view(UserView(User, db.session))


def register_database(app):
    """Register database."""
    db.init_app(app)


def register_extensions(app):
    """Register all extensions."""
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """Register all blueprints."""
    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    import logging
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)
    if not app.config['DEBUG']:
        mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                                   app.config['MAIL_USERNAME'],
                                   app.config['ADMINS'],
                                   'O_ops... %s failed!' % app.config['PROJECT'],
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]')
        )
        app.logger.addHandler(mail_handler)


def register_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500
