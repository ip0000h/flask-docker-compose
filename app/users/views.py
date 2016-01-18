from flask import flash, redirect, render_template, request, url_for
from flask.ext.login import LoginManager, login_user, logout_user

from app import app
from decorators import requires_login
from forms import LoginForm
from models import User

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
@requires_login
def logout():
    logout_user()
    return redirect(url_for('login'))
