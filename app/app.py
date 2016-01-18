# -*- coding: utf-8 -*-

# Import Flask app, modules and extensions
from flask import Flask
from flask import g, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask.ext.login import current_user, LoginManager
# import flask_profiler


# Import local modules
from admin.views import UserView, MyAdminIndexView
from database import db
from models import User
from users.decorators import requires_login


# Create a flask web app
app = Flask(__name__)

# Load settings from base file
app.config.from_object('settings.base')

# Load settings from settings file
if not app.config['TESTING']:
    app.config.from_envvar('FLASK_SETTINGS')

# Initialize db
db.init_app(app)

# #  You need to declare necessary configuration to initialize
# # flask-profiler as follows:
# app.config["flask_profiler"] = {
#     "enabled": app.config["DEBUG"],
#     "storage": {
#         "engine": "sqlite",
#     }
# }

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
login_manager.login_view = 'login_view'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


# Create a admin object
admin = Admin(app, index_view=MyAdminIndexView())
# Add views to admin object
admin.add_view(UserView(User, db.session))

# Create a tolbar object
toolbar = DebugToolbarExtension(app)


# # In order to active flask-profiler, you have to pass flask
# # app as an argument to flask-profiler.
# # All the endpoints declared so far will be tracked by flask-profiler.
# flask_profiler.init_app(app)

# Run appliation in debug mode
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'])
