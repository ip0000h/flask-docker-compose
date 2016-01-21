# -*- coding: utf-8 -*-

# Import Flask app, modules and extensions
from flask import Flask
from flask import g, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask.ext.login import current_user, LoginManager

# Import local modules
from admin.views import UserView, MyAdminIndexView
from database import db
from models import User
from users.decorators import requires_login
from users.views import users as users_blueprint


# Create a flask web app
app = Flask(__name__)

# Load settings from base file
app.config.from_object('settings.base')

# Load settings from settings file
if not app.config['TESTING']:
    app.config.from_envvar('FLASK_SETTINGS')

# Initialize db
db.init_app(app)

@app.before_request
def before_request():
    g.user = current_user


# Index page
@app.route('/')
def index():
    return render_template('index.html', page=u"It's working!")


# Secret page
@app.route('/secret')
@requires_login
def secret():
    return render_template('index.html', page=u"Secret page!")


# Create and setup logger manager object
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.views.login_view'


@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).get(userid)


# Create a admin object
admin = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap3')
# Add views to admin object
admin.add_view(UserView(User, db.session))

# Register blueprint for users app
app.register_blueprint(users_blueprint, url_prefix='/users')

# Create a tolbar object
toolbar = DebugToolbarExtension(app)


# Run appliation in debug mode
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'])
