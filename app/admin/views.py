# -*- coding: utf-8 -*-

from flask import request, redirect, url_for
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask.ext.login import current_user


class UserView(ModelView):
    """User model view for admin"""
    can_delete = False
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)
    # Don't include the standard password field when creating or editing a User
    form_excluded_columns = ('password',)
    # Automatically display human-readable names
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    """Create customized index view class that handles login & registration"""
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))
