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
    login_manager,
    mail
)
from models import User
from users.decorators import requires_login
from users.views import users as users_blueprint
from views import main_blueprint


__all__ = ['create_app']

DEFAULT_APP_NAME = 'flaskapp'


def create_app(package_name, package_path, settings_override=None,
                register_security_blueprint=True):
    """Flask app factory."""
    app = Flask(package_name, instance_relative_config=True)

    configure_app(app, settings_override)

    register_database(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    register_admin(app)
    register_extensions(app)
    register_blueprints(app)
    print(app.url_map)

    return app


def configure_app(app, config=None):
    """Configure application."""
    app.config.from_object('settings.base')
    if not app.config['TESTING']:
        app.config.from_envvar('FLASK_SETTINGS')
    else:
        app.config.from_object('settings.testing')


def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def configure_errorhandlers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("users.login", next=request.path))

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)


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
    mail.init_app(app)

def register_blueprints(app):
    """Register all blueprints."""
    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')
