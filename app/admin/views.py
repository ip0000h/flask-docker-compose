# -*- coding: utf-8 -*-

from flask import request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminUserView(ModelView):
    """User model view for admin."""
    can_delete = False
    column_list = ('username', 'email', 'password', 'last_login', 'created_at')
    column_searchable_list = ('username', 'email')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))
