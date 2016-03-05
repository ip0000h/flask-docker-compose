# -*- coding: utf-8 -*-

import psutil

from flask import request, redirect, url_for
from flask.ext.admin import expose
from flask.ext.admin.base import AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user


class MyAdminIndexView(AdminIndexView):
    """Create customized index view class that handles login & registration."""
    @expose('/')
    def index(self):
        memory_sysinfo = psutil.virtual_memory()
        cpu_sysinfo = psutil.cpu_times_percent()
        return self.render('admin/index.html',
                           cpu_sysinfo=cpu_sysinfo,
                           memory_sysinfo=memory_sysinfo)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))


class AdminUserView(ModelView):
    """User model view for admin."""
    can_delete = False
    column_list = ('username', 'email', 'password', 'last_login', 'created_at')
    column_searchable_list = ('username', 'email')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))
