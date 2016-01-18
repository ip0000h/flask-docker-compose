# -*- coding: utf-8 -*-
from functools import wraps

# Import Flask app, modules and extensions
from flask import Flask
from flask import flash, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask.ext.login import LoginManager, current_user, login_user, logout_user
# import flask_profiler


# Import local modules
from admin.views import UserView
from database import db
from forms import LoginForm
from models import User

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


# Deorated function for logging
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Logging method
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.user.id)
        login_user(user)
        flash(u"Successfully logged in as %s" % form.user.username)
        return redirect(request.args.get('next') or url_for('secret'))
    return render_template('login.html', form=form)

# Logout method
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Create and setup logger manager object
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


# Index page
@app.route('/')
def index():
    return render_template('index.html', page=u"It's working!")


# Secret page
@app.route('/secret')
@login_required
def secret():
    return render_template('index.html', page=u"Secret page!")


# Create a admin object
admin = Admin(app)
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
