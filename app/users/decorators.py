# -*- coding: utf-8 -*-

from functools import wraps

from flask import abort, redirect, request, url_for
from flask_login import current_user


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
