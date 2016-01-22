# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_user, logout_user

from database import db
from .decorators import requires_login
from .forms import LoginForm
from .models import User

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).get(form.user.id)
        login_user(user)
        flash(u"Successfully logged in as %s" % form.user.username,  "success")
        return redirect(request.args.get('next') or url_for('secret'))
    return render_template('login.html', form=form)


@users.route('/logout')
@requires_login
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for('.login'))
