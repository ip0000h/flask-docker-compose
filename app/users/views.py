# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_user, logout_user

from database import db
from users.decorators import requires_login
from users.forms import LoginForm, SignUpForm
from users.models import User

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
    return redirect(url_for('users.login'))


@users.route('/signup',methods=('GET','POST'))
def signup():
    if authutil.is_logined(request):
        return redirect('/')

    form = SignUpForm(next=request.values.get('next'))

    if form.validate_on_submit():
        username = form.username.data.encode('utf-8')
        password = form.password.data.encode('utf-8')
        email = form.email.data.encode('utf-8')

        try:
            user = backend.add_user(username,email,password)
        except BackendError,ex:
            flash('Registering error','error')
            return render_template('signup.html',form=form)

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = '/'

        return redirect(next_url)

    return render_template('signup.html',form=form)
