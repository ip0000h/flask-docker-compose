# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask
from flask import flash, request, redirect, render_template, url_for
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, current_user, login_user, logout_user

from database import db
from admin import UserView
from forms import LoginForm
from models import User

app = Flask(__name__)

app.config.from_object('settings.base')

if not app.config['TESTING']:
    app.config.from_envvar('FLASK_SETTINGS')

db.init_app(app)

admin = Admin(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.user.id)
        login_user(user)
        flash(u"Successfully logged in as %s" % form.user.username)
        return redirect(request.args.get('next') or url_for('secret'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# create and setup logger manager object
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/')
def index():
    return render_template('index.html', page=u"It's working!")


@app.route('/secret')
@login_required
def secret():
    return render_template('index.html', page=u"Secret page!")


toolbar = DebugToolbarExtension(app)

admin.add_view(UserView(User, db.session))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'])
